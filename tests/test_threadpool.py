import sys, os
sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path
import whenenvlib.threadpool
import whenenvlib.threadcontext

import unittest
import nose
import logging
import Queue
import time
log = logging.getLogger(__name__)

class threadcontext1(whenenvlib.threadcontext.threadcontext):
    def process_item(self, item):
        return item + 'a'

class threadcontext2(whenenvlib.threadcontext.threadcontext):
    def process_item(self, item):
        return item + 'b'





class TestModule_runnershell2(unittest.TestCase):
    def test_initialise(self):
        self.tp = whenenvlib.threadpool.threadPool(size = 3,
            uri= "tcp://127.0.0.1:5000")
        self.tp.activate()
        self.tp.deactivate()
    
    def test_2queue(self):
        q1 = Queue.Queue()
        q2 = Queue.Queue()
        tp1 = whenenvlib.threadpool.threadPool(size = 3,
            threadcontext_constructor=threadcontext1)
        tp2 = whenenvlib.threadpool.threadPool(size = 3,
            threadcontext_constructor=threadcontext2)
        tp1.q_in = q1
        tp2.q_in = q2
        tp1.q_out = q2
        tp2.q_out = q1
        tp1.activate()
        tp2.activate()
        q1.put('sss')
        q2.put('frog')
        time.sleep(1)
        tp1.deactivate()
        tp2.deactivate()
        
        #output = []
        #while not q1.empty():
        #    output.append(q1.get(10))
        #while not q2.empty():
        #    output.append(q2.get(10))
        
        #log.error(output)

if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
