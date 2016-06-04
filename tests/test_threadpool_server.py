import sys, os
sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path
import whenenvlib.threadpool


import unittest
import nose
import logging




class TestModule_runnershell2(unittest.TestCase):
    def test_initialise(self):
        self.tp = whenenvlib.threadpool.threadPool(size = 3,
            uri= "tcp://127.0.0.1:5000")
        self.tp.activate()
        self.tp.wait_completion()
    

if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
