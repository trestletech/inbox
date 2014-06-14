from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.interfaces import MapperOption
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm.exc import NoResultFound

import sqlalchemy.orm.session

from inbox.log import get_logger
log = get_logger()

from inbox.sqlalchemy_ext.revision import versioned_session
from inbox.models.mixins import AutoTimestampMixin

MAX_INDEXABLE_LENGTH = 191
MAX_FOLDER_NAME_LENGTH = MAX_INDEXABLE_LENGTH


# @as_declarative()
# class Base(AutoTimestampMixin):
#     """
#     Provides automated table name, primary key column, and audit timestamps.
#     """
#     id = Column(Integer, primary_key=True, autoincrement=True)


#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()

#     @declared_attr
#     def __table_args__(cls):
#         return {'extend_existing': True}


# # These are used to identify which mapper corresponds to which engine
# class MailSyncBase(Base):
#     __abstract__ = True
#     metadata = MetaData()
#     

@as_declarative()
class MailSyncBase(AutoTimestampMixin):
    """
    Provides automated table name, primary key column, and audit timestamps.
    """
    id = Column(Integer, primary_key=True, autoincrement=True)


    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __table_args__(cls):
        return {'extend_existing': True}


# # These are used to identify which mapper corresponds to which engine
# class MailSyncBase(Base):
#     __abstract__ = True
#     metadata = MetaData()
    