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
from inbox.models.namespace import Namespace





class Webhook(MailSyncBase, HasPublicID):
    """ hooks that run on new messages/events """

    namespace_id = Column(ForeignKey(Namespace.id, ondelete='CASCADE'),
                          nullable=False, index=True)
    namespace = relationship(
        'Namespace',
        primaryjoin='and_(Webhook.namespace_id==Namespace.id, '
        'Namespace.deleted_at==None)')

    lens_id = Column(ForeignKey('lens.id', ondelete='CASCADE'),
                     nullable=False, index=True)
    lens = relationship(
        'Lens',
        primaryjoin='and_(Webhook.lens_id==Lens.id, Lens.deleted_at==None)')

    callback_url = Column(Text, nullable=False)
    failure_notify_url = Column(Text)

    include_body = Column(Boolean, nullable=False)
    max_retries = Column(Integer, nullable=False, server_default='3')
    retry_interval = Column(Integer, nullable=False, server_default='60')
    active = Column(Boolean, nullable=False, server_default=true())

    min_processed_id = Column(Integer, nullable=False, server_default='0')

