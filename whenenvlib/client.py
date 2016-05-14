import zmq
import uuid
from random import choice
import time
import json

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
socket_pub = context.socket(zmq.PUB)

socket_pub.connect("tcp://127.0.0.1:5000")


socket_sub.connect("tcp://127.0.0.1:5001")

process_id = str(uuid.uuid4())


knownchannles = {
    "register" : "c2a4d156-114b-4ad8-ae87-cfa14b261bde"
    }





socket_sub.setsockopt(zmq.SUBSCRIBE, str(process_id))
socket_sub.setsockopt(zmq.SUBSCRIBE, 'frog')

master = None

poller = zmq.Poller()
poller.register(socket_sub, zmq.POLLIN)
poller.register(socket_pub, zmq.POLLIN)
    


class thingy:
    def __init__(self, process_id, identity):
        self.stop = False
        self.proc = process_id
        self.topics = {
            self.proc : self.register
        }
        self.identity = identity
        self.master = None
        
    def register(self, message):
        msg = json.loads(message)
        self.master = msg["master"]
        rec_topics = msg.get("topics")
        print msg
        if not rec_topics is None:
            print 'herde'
            envid = rec_topics.get("enviroment")
            print envid
            if not envid is None:
                self.topics[envid] = self.enviroment
                socket_sub.setsockopt(zmq.SUBSCRIBE, str(envid))
                
    def enviroment(self, message):
        print "got env" , message
        self.stop = True
        
    def sender(self):
        if self.master is None:
            socket_pub.send_multipart([knownchannles["register"], json.dumps(self.identity)])
            return
        
        
    def reciver(self):

        socks = dict(poller.poll(50))
        if socks.get(socket_sub) is not None:
            print "got message"
            topic, msg = socket_sub.recv_multipart()
            print topic, msg
            handler = self.topics.get(topic)
            if not handler is None:
                handler(msg)

    def loop(self):
        while self.stop is False:
            self.sender()
            self.reciver()



identity = {
    'identity' : process_id,
    'topics' : ['enviroment', 'executc']
}

poo = thingy(process_id, identity)
poo.loop()
