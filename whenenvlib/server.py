import zmq
import uuid
import time
import json
import model
import logging
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DatabaseError, ProgrammingError
import datetime

log = logging.getLogger("db_controler")

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

class thingy:
    def __init__(self):

        context = zmq.Context()
        self.socket_sub = context.socket(zmq.SUB)


        self.socket_pub = context.socket(zmq.PUB)

        self.socket_sub.bind("tcp://127.0.0.1:5000")


        self.socket_pub.bind("tcp://127.0.0.1:5001")

        self.process_id = str(uuid.uuid4())

        self.clients = {}

        self.topics = {}

        self.database = thingys_db()
        self.database.sqla = 'sqlite:///:memory:'
        self.database.dbstuff()

    def register(self, msg):
        print "register=%s" % (msg)
        msg = json.loads(msg)
        output = {
            'master' : str(self.process_id),
            'topics' : {}
            }
        for topic in msg["topics"]:
            topic_id = self.topics.get(topic)
            if topic_id is None:
                topic_id = str(uuid.uuid4())
                self.topics[topic] = topic_id
            output['topics'][topic] = topic_id
        self.socket_pub.send_multipart([str(msg['identity']), str(json.dumps(output))])


    def process(self, msg):
        print "process=%s" % (msg)



    def run(self):
        knownchannles = {
        "c2a4d156-114b-4ad8-ae87-cfa14b261bde" : self.register,
        }

        self.database.db_session()

        for key in knownchannles.keys():
            self.socket_sub.setsockopt(zmq.SUBSCRIBE, key)
        poller = zmq.Poller()
        poller.register(self.socket_sub, zmq.POLLIN)
        #poller.register(self.socket_pub, zmq.POLLIN)

        while True:
            socks = dict(poller.poll(50))
            if socks.get(self.socket_sub) is not None:
                print "got message"
                topic, msg = self.socket_sub.recv_multipart()
                self.database.write_msg(topic,self.process_id, msg)
                handler = knownchannles.get(topic)
                handler(msg)
            if socks.get(self.socket_pub) is not None:
                print "has message to send"
            for key in self.topics.keys():
                self.socket_pub.send_multipart([str(self.topics.get(key)), str("dddd")])
