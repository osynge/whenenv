import zmq
import uuid
import time
import json
import model
import logging
from thingys_db import thingys_db
from zmq_pub import zmq_pub
from zmq_sub import zmq_sub


log = logging.getLogger("db_controler")


class thingy:
    def __init__(self):

        self.addr_pub = "tcp://127.0.0.1:5001"
        self.addr_sub = "tcp://127.0.0.1:5000"
        

        self.process_id = str(uuid.uuid4())

        self.clients = {}

        self.topics = {}

        self.database = thingys_db()
        self.database.sqla = 'sqlite:///:memory:'
        self.database.dbstuff()


        self.zmq_sub = zmq_sub(
                addr = self.addr_sub,
                process_id = self.process_id
            )
        self.zmq_pub = zmq_pub(
                addr = self.addr_pub,
                process_id = self.process_id
            )


    def register(self, topic, msg):
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
        self.zmq_pub.send_multipart(str(msg['identity']), str(json.dumps(output)))


    def process(self, topic, msg):
        print "process=%s" % (msg)



    def run(self):
        knownchannles = {
        "c2a4d156-114b-4ad8-ae87-cfa14b261bde" : self.register,
        "675695b4-c638-40ad-95ae-0534ce5bf705" : self.process,
        }

        self.database.db_session()

        for key in knownchannles.keys():
            self.zmq_sub.add_callback(key, knownchannles.get(key))

        while True:
            self.zmq_sub.listen()
            for key in self.topics.keys():
                self.zmq_pub.send_multipart(str(self.topics.get(key)), str("dddd"))
