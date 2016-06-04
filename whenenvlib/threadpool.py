import Queue

from threading import *
import threadworker
import threadcontext
import logging

log = logging.getLogger(__name__)


def Property(func):
    return property(**func())

class threadPool(object):
    def __init__(self, **kwargs):
        self._q_in = kwargs.get('q_in', None)
        self._q_out = kwargs.get('q_out', None)
        self._context = kwargs.get('context', None)
        self.size = kwargs.get('size', None)
        self._threadworker_constructor = kwargs.get('constructor', threadworker.worker_thread)
        self._threadcontext_constructor = kwargs.get('threadcontext_constructor', threadcontext.threadcontext)
        
        
        self._array_threadworker = []
    
        self.uri = kwargs.get('uri', "tcp://127.0.0.1:5000")
        self.connect = kwargs.get('connect', True)
        
        self.context = self._threadcontext_constructor(
            uri = self.uri,
            connect = self.connect,
            q_in = self.q_in,
            q_out = self.q_out
            )
    
    def debug_info(self):
        return {
            'q_in':self.q_in.qsize(),
            'q_out':self.q_out.qsize()
        }
    
    
    def activate(self):
        log.error("activating" + str(self))
        for item in range(self.size):
            new_context = self._threadcontext_constructor(
                q_in=self.q_in,
                q_out=self.q_out,
                )
            new = self._threadworker_constructor(
                q_in=self.q_in,
                q_out=self.q_out,
                context=new_context
                )
            self._array_threadworker.append(new)
        for item in range(self.size):
            print "starting ", item
            self._array_threadworker[item].start()

    def deactivate(self):
        for item in range(self.size):
            print "starting ", item
            self._array_threadworker[item].stop()
            self._array_threadworker[item].shouldrun = False
    
        
    @Property
    def q_in():
        doc = "qin to verify hosts against"
        def fget(self):
            if hasattr(self, '_q_in'):
                if self._q_in != None:
                    return self._q_in
            self._q_in = Queue.Queue()
            return self._q_in 

        def fset(self, value):
            self._q_in = value
            
        def fdel(self):
            self._q_in = Queue.Queue()
        return locals()

    @Property
    def q_out():
        doc = "qout results"
        def fget(self):
            if hasattr(self, '_q_out'):
                if self._q_out != None:
                    return self._q_out
            self._q_out = Queue.Queue()
            return self._q_out 

        def fset(self, value):
            self._q_out = value
            
        def fdel(self):
            self._q_out = Queue.Queue()
        return locals()


    @Property
    def context():
        doc = "qout results"
        def fget(self):
            if hasattr(self, '_context'):
                if self._context != None:
                    return self._context
            self._context = self._threadcontext_constructor()
            return self._context 

        def fset(self, value):
            self._context = value
            
        def fdel(self):
            self._context = self._threadcontext_constructor()
        return locals()

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        log.error("Wait for completion of all the tasks in the queue")
        
        self.q_in.join()
        self.q_out.join()
        self.deactivate()
    
    def run(self, task):
        
        queue_empty = self.q_in.empty()
        while queue_empty is False:
            self.context.run(processed)
            
    
    def empty(self):
        return self.q_out.empty()

    def drain(self):
        queue_empty = self.q_out.empty()
        while queue_empty is False:
            try:
                processed = self.q_out.get()
                self.context.drain(processed)
            finally:
                self.q_out.task_done()
            queue_empty = self.q_out.empty()
        
