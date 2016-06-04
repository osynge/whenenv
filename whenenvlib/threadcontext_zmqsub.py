import threadcontext
import logging
import json
import Queue 

log = logging.getLogger("tp_zmqsub")

class threadcontext_zmqsub(threadcontext.threadcontext):
    
    """Base class for contexts to publish zmq
    """
    def __init__(self, **kwargs):
        threadcontext.threadcontext.__init__(self, **kwargs)
        self.deriv = "zmqsub"
        self.url = kwargs.get('uri',"tcp://127.0.0.1:5001" )
        self.subscriptions = set()
        self._cb = None
        
    
    def subscribe(self, topics):
        self.subscriptions.add(topics)
        
    def queue(self, topics, url):
        """
        This work will be done in a threadPool
        """
        log.error("queue")
        output = {
            'topic' : self.subscriptions,
            'url' : url
            }
        self.q_in.put(json.dumps(output))

    def callback(self,topic , msg):
        if self._cb is None:
            return
        output = {
            'topic' : self.subscriptions,
            'msg' : msg
            }
        msg = json.dumps(output)
        self._cb(msg)

    def process(self):
        """
        This work will be done in a thread
        """
        try:
            cntex = self.q_in.get(True, 100)
            print 'ssssssssssssssssssssssssssssssssssssssssssssssssssss'
        except Queue.Empty:
            return
        try:
            print cntex
            try:
                msg = json.loads(cntex)
            except TypeError:
                print "TypeError", cntex
                return
            except ValueError:
                print "ValueError", cntex
                return
            topic = msg.get(u'topic')
            self.context = zmq.Context()

            self.socket_sub = self.context.socket(zmq.SUB)
            self.socket_sub.connect("tcp://127.0.0.1:5001")
            for tiic in self.subscriptions:
                self.socket_sub.setsockopt(zmq.SUBSCRIBE, tiic)
            output = {
                'topic' : topic,
                'message' : message
                }
            print 'dddddddddddddddddddddddddddd'
            self.poller = zmq.Poller()
            self.poller.register(self.socket_sub, zmq.POLLIN)
            socks = dict(self.poller.poll(50))
            if socks.get(self.socket_sub) is not None:
                topic, msg = self.socket_sub.recv_multipart()
                self.queue(topic, msg)
        finally:
            self.q_in.task_done()


        
        
    def __repr__(self):
        return "<threadcontext.%s()>" % (self.deriv)
