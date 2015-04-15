from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
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

from sqlalchemy.schema import UniqueConstraint


##########################################
# makes key value tables to increase flexibility.

Base = declarative_base()



class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(100),nullable = False,unique=True)
    filepath = Column(String(100),nullable = False,unique=True)
    

class TaskProvide(Base):
    __tablename__ = 'provides'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(100),nullable = False,unique=True)
    name = Column(String(100),nullable = False,unique=True)
    fkType = Column(Integer, ForeignKey(Task.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False) 
    provides_depends = Column(Boolean(100),nullable = False,unique=True)


class TaskDepend(Base):
    __tablename__ = 'Depends'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(100),nullable = False,unique=True)
    name = Column(String(100),nullable = False,unique=True)
    fkType = Column(Integer, ForeignKey(Task.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False) 
    Depends_depends = Column(Boolean(100),nullable = False,unique=True)





class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(100),nullable = False,unique=True)
    name = Column(String(100),nullable = False,unique=True)
    lastexecuted = Column(DateTime,nullable = True)


class JobProxides(Base):
    __tablename__ = 'jobprovides'
    id = Column(Integer, primary_key=True)
    fkJob = Column(Integer, ForeignKey(Job.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False) 
    fkProvide = Column(Integer, ForeignKey(Job.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False) 
