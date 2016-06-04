import threadcontext
import zmq
import json




class Error(Exception):
    """
    Error
    """

    def __str__(self):
        doc = self.__doc__.strip()
        return ': '.join([doc] + [str(a) for a in self.args])



class threadcontext_zmqpub(threadcontext.threadcontext):
    
    """Base class for contexts to publish zmq
    """
    def __init__(self, **kwargs):
        threadcontext.threadcontext.__init__(self, **kwargs)
        self.deriv = "zmqpub"
        
        if self.uri is None:
            raise Error('uri is None',self.uri)
        self.context = zmq.Context()
        self.socket_pub = self.context.socket(zmq.PUB)
        
        if self.connect:
            self.socket_pub.connect(self.uri)
    
    
    def queue(self, topic, message):
        """
        This work will be done in a threadPool
        """
        output = {
            'topic' : topic,
            'message' : message
            }
        self.q_in.put(json.dumps(output))
        return 1

    def process(self):
        """
        This work will be done in a thread
        """
        try:
            cntx = self.q_in.get(10)
            if cntx is None:
                return
            try:
                msg = json.loads(cntx)
            except TypeError:
                print "cntx TypeError", cntx
                return
            #print "msg=%s" % (msg)
            topic = str(msg['topic'])
            message = str(msg['message'])
            self.socket_pub.send_multipart((topic, message))
            output = {
                'topic' : topic,
                'message' : message
                }
            return self.q_out.put(json.dumps(output))
        finally:
            self.q_in.task_done()
        

    def drain(self, context_in):
        """
        This work will be done in threadPool post operation
        """
        return None
