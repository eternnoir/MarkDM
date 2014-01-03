from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from hashlib import *

import os

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from sqlalchemy.schema import *

from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'editors', 'edit') ]
    def __init__(self, request):
        pass

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

class Repos(Base):
    __tablename__ = 'repo'
    id = Column(Integer, primary_key=True)
    name = Column(Text)



class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer,
                   Sequence('groups_seq_id', optional=True),
                   primary_key=True)
    groupname = Column(Text, unique=True)

    def __init__(self, groupname):
        self.groupname = groupname

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,
                   Sequence('users_seq_id', optional=True),
                   primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    mygroups = relationship(Groups, secondary='user_group')

    def __init__(self, user, password):
        self.username = user
        self._set_password(password)

    @classmethod
    def by_id(cls, userid):
        return DBSession.query(Users).filter(Users.id==userid).first()

    @classmethod
    def by_username(cls, username):
        return DBSession.query(Users).filter(Users.username==username).first()

    def _set_password(self, password):
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(str(password_8bit) + str(salt.hexdigest()))
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self.password = hashed_password

    def validate_password(self, password):
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

user_group_table = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey(Users.id)),
    Column('group_id', Integer, ForeignKey(Groups.id)),
)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
