import zmq
import uuid
import time

import time
import json
from thingys_db import thingys_db
import logging
import threadpool_zmqpub
import threadpool_zmqsub

log = logging.getLogger(__name__)


class qclient:
    def __init__(self, **kwargs):
        self.uri = kwargs.get('uri', "tcp://127.0.0.1:5000")
        
        self.process_id = str(uuid.uuid4())

        self.tp_zmqpub = threadpool_zmqpub.tp_zmqpub(
            uri = self.uri,
            )



        self.tp_zmqsub = threadpool_zmqsub.tp_zmqsub(
            uri = "tcp://127.0.0.1:5001"
            
            )
        self.tp_zmqsub.subscribe([self.process_id])
        
        self.knownchannles = {
        "c2a4d156-114b-4ad8-ae87-cfa14b261bde" : None,
        "675695b4-c638-40ad-95ae-0534ce5bf705" : None,
        }
        for key in  self.knownchannles:
            self.tp_zmqsub.subscribe(key)

        
        self.counter = 0
        
    def run(self):
        self.identity = {
            'identity' : self.process_id,
            'topics' : ['enviroment', 'execute']
        }
        self.tp_zmqpub.activate()
        self.tp_zmqsub.activate()
        self.loop()
        print 'pub', self.tp_zmqpub.debug_info()
        print 'sub', self.tp_zmqsub.debug_info()
        self.tp_zmqpub.drain()
        self.tp_zmqsub.drain()
        print 'pub', self.tp_zmqpub.debug_info()
        print 'sub', self.tp_zmqsub.debug_info()
        
        self.tp_zmqpub.wait_completion()
        self.tp_zmqsub.wait_completion()

    def sendmsgs(self):
        log.error("sendmsgs")
        self.tp_zmqpub.send_multipart( "c2a4d156-114b-4ad8-ae87-cfa14b261bde" , json.dumps(self.identity))
        self.tp_zmqpub.send_multipart( "675695b4-c638-40ad-95ae-0534ce5bf705" , json.dumps(self.identity))
        self.tp_zmqpub.drain()
        
    def recivemsg(self):
        #log.error("recivemsg")
        self.tp_zmqsub.drain()
        
        
        

    def loop(self):
        while self.counter < 10:
            print 'sub', self.tp_zmqsub.debug_info()
            self.sendmsgs()
            self.recivemsg ()
            self.counter = self.counter + 1
            print self.counter
            time.sleep(1)
            
        

    def subscribe_topic(self,topic):
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, topic)

