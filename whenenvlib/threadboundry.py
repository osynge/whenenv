
class boundry(object):
    def __init__(self, **kwargs):
        self.threadpoolsize = kwargs.get('identifier', 10)
        
        

    def initialise_threadpool():
        self.threadqueue = Queue.Queue()

class boundry_database(boundry):
    def __init__(self, **kwargs):
        boundry.__init__(self)
        self.threadpoolsize = kwargs.get('identifier', 1)





