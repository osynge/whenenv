import Queue
import threadcontext

from threading import *
import logging

log = logging.getLogger(__name__)

def Property(func):
    return property(**func())

class worker_thread(Thread):
    def __init__(self, **kwargs):
        Thread.__init__(self)
        self._item = kwargs.get('item', None)
        self._q_in = kwargs.get('q_in', None)
        self._q_out = kwargs.get('q_out', None)
        self._context = kwargs.get('context', None)
        self._context_constructor = kwargs.get('construct.context', None)
        self._stop = Event()
    
    def stop(self):
        self._stop.set()
    
    def should_run(self):
        return not self._stop.isSet()
    
    @Property
    def item():
        doc = "trustanchor_type to verify hosts against"
        def fget(self):
            if hasattr(self, '_item'):
                if self._item != None:
                    return self._item
            return None

        def fset(self, value):
            self._item = value
            
        def fdel(self):
            self._item = Queue.Queue()
        return locals()


    @Property
    def q_in():
        doc = "trustanchor_type to verify hosts against"
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
        doc = "trustanchor_type to verify hosts against"
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


    @property
    def context(self):
        if hasattr(self, '_context'):
            if self._context != None:
                return self._context
        self._context = threadcontext.threadcontext(
            q_in = self.q_in,
            q_out = self.q_out
            )
        return self._context 

    @context.setter
    def context(self, value):
        self._context = value
    
    
    @property
    def shouldrun(self):
        if hasattr(self.context, 'shouldrun'):
            return self.context.shouldrun
        return False

    @shouldrun.setter
    def shouldrun(self, value):
        self.context.shouldrun = value
    


    def run_task(self):
        self.context.process()
        
        
    
    def run(self):
        print "running"
        self.shouldrun = True
        while self.should_run():
            self.run_task()



