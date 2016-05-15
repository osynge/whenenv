import uuid
import time
import json
import model
import logging


from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DatabaseError, ProgrammingError
import datetime


class thingys_db:
    def __init_(self):
        self.sqla = kwargs.get('sqlalchamy', None)
        self.dblogging_echo = True
        if self.sqla is None:
            if 'WHENENV_RDBMS' in os.environ:
                self.sqla = os.environ['WHENENV_RDBMS']

    def dbstuff(self):
        if self.sqla is None:
            raise Errror("no sqal")
        dblogging_echo = True
        self.engine = create_engine(self.sqla, echo=dblogging_echo)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)

    def db_session(self):
        instruct_topics = [{
            'number' : 367,
            'name' : 'introductions',
            'uuid' : '3ff7273c-8778-49ad-9ed9-5045ffef1eb4'
        },{
            'number' : 765,
            'name' : 'whenenv_stdout'
        }]

        self.setup_topics( instruct_topics)
        instruct_hosts = [{
            'number' : 367,
            'name' : 'introductions',
            'uuid' : '0afd33e0-90a0-4da6-8b2b-344ee4973914'
        }]

        self.setup_hosts( instruct_hosts)

    def setup_topics(self, topic_itterator):
        session = self.SessionFactory()
        for instructions in topic_itterator:
            print instructions
            new_item =  model.zmqPubTopic(**instructions)
            session.add(new_item)
            try:
                session.commit()
            except IntegrityError:
                print "IntegrityError"
                session = self.SessionFactory()
            except InvalidRequestError:
                session = self.SessionFactory()
                print "InvalidRequestError"
    def setup_hosts(self, topic_itterator):
        session = self.SessionFactory()
        for instructions in topic_itterator:



            session.query(model.zmqClient)
            new_item =  model.zmqClient(**instructions)
            session.add(new_item)
            try:
                session.commit()
            except IntegrityError:
                session = self.SessionFactory()
            except InvalidRequestError:
                session = self.SessionFactory()

    def write_msg(self,topic, recivedby, msg):
        session = self.SessionFactory()

        now = datetime.datetime.utcnow()
        instructions = {
            'topic' : topic,
            'recivedby' : recivedby,
            'created' : now,
            'expires' : now,
            'identifier' : str(uuid.uuid4())

        }
        new_item =  model.zmqClientInteraction(**instructions)
        session.add(new_item)
        try:
            session.commit()
        except IntegrityError:
            log.error("IntegrityError")
            session = self.SessionFactory()
        except InvalidRequestError:
            session = self.SessionFactory()
