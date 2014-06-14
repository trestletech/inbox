""" Namespace object and related functions.

All functions in this file should take `namespace_id` as their first
argument and make sure to limit the action based on it!
"""

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
from inbox.models.base import MailSyncBase
from inbox.models.mixins import HasPublicID





class Namespace(MailSyncBase, HasPublicID):
    """ A way to do grouping / permissions, basically. """
    # NOTE: only root namespaces have account backends
    account_id = Column(Integer,
                        ForeignKey('account.id', ondelete='CASCADE'),
                        nullable=True)
    # really the root_namespace
    account = relationship('Account',
                           lazy='joined',
                           backref=backref('namespace', uselist=False,
                                           primaryjoin='and_('
                                           'Account.id==Namespace.account_id, '
                                           'Namespace.deleted_at.is_(None))'),
                           uselist=False,
                           primaryjoin='and_('
                           'Namespace.account_id == Account.id, '
                           'Account.deleted_at.is_(None))')

    # invariant: imapaccount is non-null iff type is root
    type = Column(Enum('root', 'shared_folder'), nullable=False,
                  server_default='root')

    @property
    def email_address(self):
        if self.account is not None:
            return self.account.email_address



