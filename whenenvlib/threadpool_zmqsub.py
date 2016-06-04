import threadpool
import threadcontext_zmqsub
import logging

log = logging.getLogger("tp_zmqsub")



class Error(Exception):
    """
    Error
    """

    def __str__(self):
        doc = self.__doc__.strip()
        return ': '.join([doc] + [str(a) for a in self.args])





class tp_zmqsub(threadpool.threadPool):
    """Base class for contexts to publish zmq
    """
    def __init__(self, **kwargs):
    
        self._threadcontext_constructor = kwargs.get('threadcontext_constructor', threadcontext_zmqsub.threadcontext_zmqsub)
        kwargs['threadcontext_constructor'] = self._threadcontext_constructor
        threadpool.threadPool.__init__(self, **kwargs)
        log.info("kwargs", kwargs)
        self.addr = kwargs.get('addr', None)
        self.size = kwargs.get('size', 1)
        self.zmq_context = kwargs.get('zmq_context', None)
        self.uri = kwargs.get('uri', "tcp://127.0.0.1:5000")
        self.connect = kwargs.get('connect', 1)
        self.subscriptions = set()
        
        
        

   
        
    def subscribe(self, topiclist):
        if topiclist == None:
            return
        for item in topiclist:
            self.subscriptions.add(item)
    
    
    
    def drain(self):
        threadpool.threadPool.drain(self)




    def run(self):
        
        threadpool.threadPool.run(self)
