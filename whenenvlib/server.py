import zmq
import uuid
import time
import json
import model
import logging
from thingys_db import thingys_db
from zmq_pub import zmq_pub

log = logging.getLogger("db_controler")



class thingy:
    def __init__(self):

        context = zmq.Context()
        self.addr_pub = "tcp://127.0.0.1:5001"

        self.socket_sub = context.socket(zmq.SUB)


        self.socket_sub.bind("tcp://127.0.0.1:5000")

        self.process_id = str(uuid.uuid4())

        self.clients = {}

        self.topics = {}

        self.database = thingys_db()
        self.database.sqla = 'sqlite:///:memory:'
        self.database.dbstuff()


        self.zmq_pub = zmq_pub(
                addr = self.addr_pub,
                process_id = self.process_id
            )


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
        self.zmq_pub.send_multipart(str(msg['identity']), str(json.dumps(output)))


    def process(self, msg):
        print "process=%s" % (msg)



    def run(self):
        knownchannles = {
        "c2a4d156-114b-4ad8-ae87-cfa14b261bde" : self.register,
        "675695b4-c638-40ad-95ae-0534ce5bf705" : self.process,
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
            #if socks.get(self.socket_pub) is not None:
            #    print "has message to send"
            for key in self.topics.keys():
                self.zmq_pub.send_multipart(str(self.topics.get(key)), str("dddd"))
