import Queue
import logging

log = logging.getLogger(__name__)
import threading


class threadcontext(object):
    """Base class for contexts
    
    Contexts are chains of three functions.
    
    the output of the queue()
    
    """
    def __init__(self, **kwargs):
        
        self.deriv = "base"
        self.q_in = kwargs.get('q_in', None)
        self.q_out = kwargs.get('q_out', None)
        self.connect = kwargs.get('connect', True)
        self.uri = kwargs.get('uri', "tcp://127.0.0.1:5000")
        
    @property
    def shouldrun(self):
        if hasattr(self, '_shouldrun'):
            if self._shouldrun is False:
                return False
        return True

    @shouldrun.setter
    def shouldrun(self, value):
        self._shouldrun = True
        if value is False:
            self._shouldrun = False
        return




    def queue(self):
        """
        This work will be done in a threadPool
        """
        self.q_in.put(json.dumps([]))
        return 1
    
    
    def process_item(self, item):
        return item


    def process(self):
        """
        This work will be done in a thread
        """
        
        try:
            raw = self.q_in.get(True, 1)
        except Queue.Empty:
            return
        try:
            refined = self.process_item(raw)
            self.q_out.put(refined, True, 1)
        finally:
            self.q_in.task_done()


    def drain(self):
        """
        This work will be done outside the threadPool post operation
        """
        queue_empty = self.q_out.empty()
        if queue_empty is False:
            try:
                cntex = self.q_out.get(True, 10)
            except Queue.Empty:
                return self.context

            try:
                pass    
            finally:
                self.q_out.task_done()        
        return self.context


    def __repr__(self):
        return "<threadcontext.%s()>" % (self.deriv)
