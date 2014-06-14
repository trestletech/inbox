import itertools
import os
import re
import json

from hashlib import sha256
from datetime import datetime
import bson

from sqlalchemy import (Column, Integer, BigInteger, String, DateTime, Boolean,
                        Enum, ForeignKey, Text, func, event, and_, or_, asc,
                        desc)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import (reconstructor, relationship, backref, deferred,
                            validates, object_session)
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import BLOB
from sqlalchemy.sql.expression import true, false

from inbox.log import get_logger
log = get_logger()

from inbox.config import config
from inbox.sqlalchemy_ext.util import generate_public_id
from inbox.util.encoding import base36decode
from inbox.util.file import Lock, mkdirp
from inbox.util.html import (plaintext2html, strip_tags, extract_from_html,
                             extract_from_plain)
from inbox.util.misc import load_modules
from inbox.util.cryptography import encrypt_aes, decrypt_aes
from inbox.sqlalchemy_ext.util import (JSON, BigJSON, Base36UID,
                                       maybe_refine_query)
from inbox.sqlalchemy_ext.revision import Revision, gen_rev_role
from inbox.basicauth import AUTH_TYPES

from inbox.models.roles import Blob
from inbox.models.mixins import HasPublicID
from inbox.models.transaction import HasRevisions
from inbox.models.base import MailSyncBase
from inbox.models.mixins import HasPublicID
from inbox.models.transaction import HasRevisions


class Message(MailSyncBase, HasRevisions, HasPublicID):
    # XXX clean this up a lot - make a better constructor, maybe taking
    # a flanker object as an argument to prefill a lot of attributes

    # Do delete messages if their associated thread is deleted.
    thread_id = Column(Integer, ForeignKey('thread.id', ondelete='CASCADE'),
                       nullable=False)
    thread = relationship(
        'Thread',
        primaryjoin='and_(Message.thread_id == Thread.id, '
                    'Thread.deleted_at.is_(None))',
        backref=backref('messages',
                        primaryjoin='and_('
                        'Message.thread_id == Thread.id, '
                        'Message.deleted_at.is_(None))',
                        order_by='Message.received_date',
                        info={'versioned_properties': ['id']}))

    from_addr = Column(JSON, nullable=True)
    sender_addr = Column(JSON, nullable=True)
    reply_to = Column(JSON, nullable=True)
    to_addr = Column(JSON, nullable=True)
    cc_addr = Column(JSON, nullable=True)
    bcc_addr = Column(JSON, nullable=True)
    in_reply_to = Column(JSON, nullable=True)
    message_id_header = Column(String(255), nullable=True)
    subject = Column(Text, nullable=True)
    received_date = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    data_sha256 = Column(String(255), nullable=True)

    mailing_list_headers = Column(JSON, nullable=True)

    is_draft = Column(Boolean, server_default=false(), nullable=False)
    is_read = Column(Boolean, server_default=false(), nullable=False)

    # Most messages are short and include a lot of quoted text. Preprocessing
    # just the relevant part out makes a big difference in how much data we
    # need to send over the wire.
    # Maximum length is determined by typical email size limits (25 MB body +
    # attachments on Gmail), assuming a maximum # of chars determined by
    # 1-byte (ASCII) chars.
    # NOTE: always HTML :)
    sanitized_body = Column(Text(length=26214400), nullable=False)
    snippet = Column(String(191), nullable=False)
    SNIPPET_LENGTH = 191

    # we had to replace utf-8 errors before writing... this might be a
    # mail-parsing bug, or just a message from a bad client.
    decode_error = Column(Boolean, server_default=false(), nullable=False)

    # only on messages from Gmail
    g_msgid = Column(BigInteger, nullable=True, index=True)
    g_thrid = Column(BigInteger, nullable=True, index=True)

    # The uid as set in the X-INBOX-ID header of a sent message we create
    inbox_uid = Column(String(64), nullable=True)

    # In accordance with JWZ (http://www.jwz.org/doc/threading.html)
    references = Column(JSON, nullable=True)

    @property
    def namespace(self):
        return self.thread.namespace

    def calculate_sanitized_body(self):
        plain_part, html_part = self.body
        # TODO: also strip signatures.
        if html_part:
            assert '\r' not in html_part, "newlines not normalized"
            stripped = extract_from_html(html_part.encode('utf-8')).decode('utf-8').strip()
            self.sanitized_body = unicode(stripped)
            self.calculate_html_snippet(self.sanitized_body)
        elif plain_part:
            stripped = extract_from_plain(plain_part).strip()
            self.sanitized_body = plaintext2html(stripped, False)
            self.calculate_plaintext_snippet(stripped)
        else:
            self.sanitized_body = u''
            self.snippet = u''

    def calculate_html_snippet(self, text):
        text = text.replace('<br>', ' ').replace('<br/>', ' '). \
            replace('<br />', ' ')
        text = strip_tags(text)
        self.calculate_plaintext_snippet(text)

    def calculate_plaintext_snippet(self, text):
        self.snippet = ' '.join(text.split())[:self.SNIPPET_LENGTH]

    @property
    def body(self):
        """ Returns (plaintext, html) body for the message, decoded. """
        assert self.parts, \
            "Can't calculate body before parts have been parsed"

        plain_data = None
        html_data = None

        for part in self.parts:
            if part.content_type == 'text/html':
                html_data = part.data.decode('utf-8')
                break
        for part in self.parts:
            if part.content_type == 'text/plain':
                plain_data = part.data.decode('utf-8')
                break

        return plain_data, html_data

    def trimmed_subject(self):
        s = self.subject
        if s[:4] == u'RE: ' or s[:4] == u'Re: ':
            s = s[4:]
        return s

    @property
    def prettified_body(self):
        html_data = self.sanitized_body

        prettified = None
        if 'font:' in html_data or 'font-face:' \
                in html_data or 'font-family:' in html_data:
            prettified = html_data
        else:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'message_template.html')
            with open(path, 'r') as f:
                # template has %s in it. can't do format because python
                # misinterprets css
                prettified = f.read() % html_data

        return prettified

    @property
    def mailing_list_info(self):
        return self.mailing_list_headers

    @property
    def headers(self):
        """ Returns headers for the message, decoded. """
        assert self.parts, \
            "Can't provide headers before parts have been parsed"

        headers = self.parts[0].data
        json_headers = json.JSONDecoder().decode(headers)

        return json_headers

    @property
    def folders(self):
        return self.thread.folders

    discriminator = Column('type', String(16))
    __mapper_args__ = {'polymorphic_on': discriminator,
                       'polymorphic_identity': 'message'}


class SpoolMessage(Message):
    """
    Messages created by this client.

    Stored so they are immediately available to the user. They are reconciled
    with the messages we get from the remote backend in a subsequent sync.
    """
    id = Column(Integer, ForeignKey('message.id', ondelete='CASCADE'),
                primary_key=True)

    created_date = Column(DateTime)
    is_sent = Column(Boolean, server_default=false(), nullable=False)

    state = Column(Enum('draft', 'sending', 'sending failed', 'sent'),
                   server_default='draft', nullable=False)

    # Null till reconciled.
    # Deletes should not be cascaded! i.e. delete on remote -> delete the
    # resolved_message *only*, not the original SpoolMessage we created.
    # We need this to correctly maintain draft versions (created on
    # update_draft())
    resolved_message_id = Column(Integer,
                                 ForeignKey('message.id'),
                                 nullable=True)
    resolved_message = relationship(
        'Message',
        primaryjoin='and_('
        'SpoolMessage.resolved_message_id==remote(Message.id), '
        'remote(Message.deleted_at)==None)',
        backref=backref('spooled_messages', primaryjoin='and_('
                        'remote(SpoolMessage.resolved_message_id)==Message.id,'
                        'remote(SpoolMessage.deleted_at)==None)'))

    ## FOR DRAFTS:

    # For non-conflict draft updates: versioning
    parent_draft_id = Column(Integer,
                             ForeignKey('spoolmessage.id', ondelete='CASCADE'),
                             nullable=True)
    parent_draft = relationship(
        'SpoolMessage',
        remote_side=[id],
        primaryjoin='and_('
        'SpoolMessage.parent_draft_id==remote(SpoolMessage.id), '
        'remote(SpoolMessage.deleted_at)==None)',
        backref=backref(
            'child_draft', primaryjoin='and_('
            'remote(SpoolMessage.parent_draft_id)==SpoolMessage.id,'
            'remote(SpoolMessage.deleted_at)==None)',
            uselist=False))

    # For conflict draft updates: copy of the original is created
    # We don't cascade deletes because deleting a draft should not delete
    # the other drafts that are updates to the same original.
    draft_copied_from = Column(Integer,
                               ForeignKey('spoolmessage.id'),
                               nullable=True)

    # For draft replies: the 'copy' of the thread it is a reply to.
    replyto_thread_id = Column(Integer, ForeignKey('draftthread.id',
                               ondelete='CASCADE'), nullable=True)
    replyto_thread = relationship(
        'DraftThread', primaryjoin='and_('
        'SpoolMessage.replyto_thread_id==remote(DraftThread.id),'
        'remote(DraftThread.deleted_at)==None)',
        backref=backref(
            'draftmessage', primaryjoin='and_('
            'remote(SpoolMessage.replyto_thread_id)==DraftThread.id,'
            'remote(SpoolMessage.deleted_at)==None)',
            uselist=False))


    __mapper_args__ = {'polymorphic_identity': 'spoolmessage',
                       'inherit_condition': id == Message.id}

