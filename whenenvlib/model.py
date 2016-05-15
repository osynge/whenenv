from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime,LargeBinary
from sqlalchemy.orm import mapper

from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref
try:
    from sqlalchemy.orm import relationship
except:
    from sqlalchemy.orm import relation as relationship


from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

import uuid
Base = declarative_base()

""" Things to change in data base.
1) Images definitions need more status flags.
2)
"""



class zmqPubTopic(Base):
    """This table defines the Human Name for the Endorser."""
    __tablename__ = 'ZMQCLIENT_TOPIC'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(50))
    uuid = Column(String(50))
    def __init__(self, **kwargs):
        self.number = kwargs.get('number', None)
        self.name = kwargs.get('name', None)
        self.uuid = kwargs.get('uuid', None)
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())
    def __repr__(self):
        return "<zmqPubTopic(%s,%s,%s)>" % (self.number,self.name,self.id)


class zmqClient(Base):
    """About the Client."""
    __tablename__ = 'ZMQCLIENT_CLIENT'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50),unique=True,nullable = False)
    def __init__(self, **kwargs):
        print 'here we are', kwargs
        self.uuid = kwargs.get('uuid', None)
        print 'here we are', self.uuid
    def __repr__(self):
        return "<zmqClient(%s,%s)>" % (self.uuid,self.id)


class zmqClientInteraction(Base):
    """This table defines the Human Name for the Endorser."""
    __tablename__ = 'ZMQCLIENT_INTERACTION'
    id = Column(Integer, primary_key=True)
    identifier = Column(String(50),unique=True,nullable = False)
    topic = Column(Integer, ForeignKey(zmqPubTopic.id, onupdate="CASCADE", ondelete="CASCADE"))
    recivedby = Column(Integer, ForeignKey(zmqClient.id, onupdate="CASCADE", ondelete="CASCADE"))
    created = Column(DateTime,nullable = False)
    expires = Column(DateTime,nullable = False)

    def __init__(self, **kwargs):
        self.identifier = kwargs.get('identifier', None)
        self.topic = kwargs.get('topic', None)
        self.recivedby = kwargs.get('recivedby', None)
        self.created = kwargs.get('created', None)
        self.expires = kwargs.get('expires', None)

    def __repr__(self):
        return "<zmqClientInteraction(%s,%s,%s,%s)>" % (self.identifier,self.topic,self.recivedby, self.id)


class zmqClientMetadata(Base):
    """About the Client."""
    __tablename__ = 'ZMQCLIENT_CLIENT_META DATA'
    id = Column(Integer, primary_key=True)
    client_version = Column(String(50),nullable = False)
    osname = Column(String(50),unique=True,nullable = False)
    osversion = Column(String(50),unique=True,nullable = False)
    osfamily = Column(String(50),unique=True,nullable = False)
    unix_id = Column(Integer)
    unix_gid = Column(Integer)
    role = Column(String(50),unique=True,nullable = False)
    expires = Column(Integer, ForeignKey(zmqClientInteraction.id, onupdate="CASCADE", ondelete="CASCADE"))
    def __init__(self, **kwargs):
        self.client_version = kwargs.get('client_version', None)
        self.osname = kwargs.get('osname', None)
        self.osversion = kwargs.get('osversion', None)
        self.osfamily = kwargs.get('osfamily', None)
        self.unix_id = kwargs.get('unix_id', None)
        self.unix_gid = kwargs.get('unix_gid', None)
        self.expires = kwargs.get('expires', None)


def init(engine):
    Base.metadata.create_all(engine)
