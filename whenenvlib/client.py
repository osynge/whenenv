import zmq
import uuid
from random import choice
import time
import json
from thingys_db import thingys_db
import logging
import threadpool_zmqpub

log = logging.getLogger(__name__)


class thingy:
    def __init__(self, process_id, identity):
        self.stop = False
        self.proc = process_id
        self.topics = {
            self.proc : self.register
        }
        self.identity = identity
        self.master = None

        self.database = thingys_db()
        self.database.sqla = 'sqlite:///:memory:'
        self.database.dbstuff()

    def call_register_topic_cb(self,topic):
        if self.register_topic_cb == None:
            return
        return self.register_topic_cb(topic)


    def register(self, message):
        msg = json.loads(message)
        self.master = msg["master"]
        rec_topics = msg.get("topics")
        log.info("msg=", msg)
        if not rec_topics is None:
            print 'herde'
            envid = rec_topics.get("enviroment")
            print envid
            if not envid is None:
                self.topics[envid] = self.enviroment
                #socket_sub.setsockopt(zmq.SUBSCRIBE, str(envid))
                self.call_register_topic_cb(str(envid))


    def enviroment(self, message):
        print "got env" , message
        self.stop = True




class thingy_ctrl:
    def __init__(self, **kwargs):
        self.context = zmq.Context()
        self.socket_sub = self.context.socket(zmq.SUB)
        self.socket_pub = self.context.socket(zmq.PUB)
        self.socket_pub.connect("tcp://127.0.0.1:5000")
        self.socket_sub.connect("tcp://127.0.0.1:5001")
        self.process_id = str(uuid.uuid4())
        self.knownchannles = {
            "register" : "c2a4d156-114b-4ad8-ae87-cfa14b261bde"
            }
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, self.process_id)
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, 'frog')

        master = None

        self.poller = zmq.Poller()
        self.poller.register(self.socket_sub, zmq.POLLIN)
        self.poller.register(self.socket_pub, zmq.POLLIN)


        self.fred = threadpool_zmqpub.tp_zmqpub(
            zmq_pub = self.socket_pub
            
            )
        self.fred.zmq_pub= self.socket_pub
        self.fred.activate()



    def run(self):
        self.identity = {
            'identity' : self.process_id,
            'topics' : ['enviroment', 'execute']
        }

        self.poo = thingy(self.process_id, self.identity)
        self.poo.register_topic_cb = self.subscribe_topic
        self.loop()


    def sendmsgs(self):
        if self.poo.master is None:
            self.socket_pub.send_multipart([self.knownchannles["register"], json.dumps(self.identity)])
            self.fred.send_multipart(self.knownchannles["register"], json.dumps(self.identity))

    def recivemsg(self):
        socks = dict(self.poller.poll(50))
        if socks.get(self.socket_sub) is not None:
            print "got message"
            topic, msg = self.socket_sub.recv_multipart()
            print topic, msg
            self.poo.database.write_msg(topic, self.process_id, msg)
            handler = self.poo.topics.get(topic)
            if not handler is None:
                handler(msg)

    def loop(self):
        while self.poo.stop is False:
            self.sendmsgs()
            self.recivemsg()


    def subscribe_topic(self,topic):
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, topic)

