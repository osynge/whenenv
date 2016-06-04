import sys, os
sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path
import whenenvlib.threadcontext


import unittest
import nose
import logging




class TestModule_runnershell2(unittest.TestCase):
    def test_initialise(self):
        context = whenenvlib.threadcontext.threadcontext()
        assert context.shouldrun == True
        
        context.shouldrun = False
        assert context.shouldrun is False
        context.shouldrun = "elephant"
        print context.shouldrun
        assert context.shouldrun == True
        
    

if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
