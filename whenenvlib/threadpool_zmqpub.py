import threadpool
import threadcontext_zmqpub
import logging
import json

log = logging.getLogger("tp_zmqpub")

class tp_zmqpub(threadpool.threadPool):
    """Base class for contexts to publish zmq
    """
    def __init__(self, **kwargs):
        self._threadcontext_constructor = kwargs.get('threadcontext_constructor', threadcontext_zmqpub.threadcontext_zmqpub)
        kwargs['threadcontext_constructor'] = self._threadcontext_constructor
        threadpool.threadPool.__init__(self, **kwargs)
        log.error("_threadcontext_constructor" + str(self._threadcontext_constructor))
        log.info("kwargs", kwargs)
        self.addr = kwargs.get('addr', None)
        self.size = kwargs.get('size', 1)
        self.uri = kwargs.get('uri', "tcp://127.0.0.1:5000")
        self.connect = kwargs.get('connect', 1)
        
        
              
        self.context =  self._threadcontext_constructor(
            uri = self.uri,
            connect = self.connect,
            q_in = self.q_in,
            q_out = self.q_out
            )
    
          
        
    def send_multipart(self, topics, message):
        log.info("topics=%s msg=%s" % (topics, message))
        
        output = {
            'topic' : topics,
            'message' : message
            }
        msg = json.dumps(output)
        
        qcntx = self.q_in.put(msg)
        

    
    def drain(self):
        while True:
            cntex = self.q_out.get(True, 10)
            try:
                log.info("topics=%s%s" % (cntex))
            finally:
                self.q_out.task_done()
        return True
    
    def drain(self):
        threadpool.threadPool.drain(self)
