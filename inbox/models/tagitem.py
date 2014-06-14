
from sqlalchemy import (Column, Integer, BigInteger, String, DateTime, Boolean,
                        Enum, ForeignKey, func, event, and_, or_, asc,
                        desc)
from sqlalchemy.orm import (relationship, backref,
                            validates, object_session)
from sqlalchemy.sql.expression import false, true

from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.schema import UniqueConstraint


from inbox.sqlalchemy_ext.util import generate_public_id
from inbox.util.html import (plaintext2html, strip_tags, extract_from_html,
                             extract_from_plain)

from inbox.models.transaction import HasRevisions
from inbox.models.base import MailSyncBase
from inbox.models.namespace import Namespace



from inbox.models.thread import Tag
from inbox.models.thread import Thread



class TagItem(MailSyncBase):
    """Mapping between user tags and threads."""
    thread_id = Column(Integer, ForeignKey(Thread.id), nullable=False)
    tag_id = Column(Integer, ForeignKey(Tag.id), nullable=False)
    thread = relationship(
        'Thread',
        backref=backref('tagitems',
                        collection_class=set,
                        cascade='all, delete-orphan',
                        primaryjoin='and_(TagItem.thread_id==Thread.id, '
                                    'TagItem.deleted_at.is_(None))',
                        info={'versioned_properties': ['tag_id',
                                                       'action_pending']}),
        primaryjoin='and_(TagItem.thread_id==Thread.id, '
        'Thread.deleted_at.is_(None))')
    tag = relationship(
        Tag,
        backref=backref('tagitems',
                        primaryjoin='and_('
                        'TagItem.tag_id  == Tag.id, '
                        'TagItem.deleted_at.is_(None))',
                        cascade='all, delete-orphan'),
        primaryjoin='and_(TagItem.tag_id==Tag.id, '
        'Tag.deleted_at.is_(None))')

    # This flag should be set by calling code that adds or removes a tag from a
    # thread, and wants a syncback action to be associated with it as a result.
    @property
    def action_pending(self):
        if not hasattr(self, '_action_pending'):
            self._action_pending = False
        return self._action_pending

    @action_pending.setter
    def action_pending(self, value):
        self._action_pending = value

    @property
    def namespace(self):
        return self.thread.namespace