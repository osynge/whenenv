import zmq

class zmq_sub:
    def __init__(self, **kwargs):

        self.zmq_context = kwargs.get('zmq_context', None)
        if self.zmq_context is None:
            self.zmq_context = zmq.Context()

        self.socket_sub = self.zmq_context.socket(zmq.SUB)
        self.addr = kwargs.get('addr', None)
        self.socket_sub.bind(self.addr)
        self.process_id = kwargs.get('process_id', None)
        self.clients = {}
        self.topics = {}
        self.callbacks = {}
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, 'sdsd')

    def add_callback(self, topic, callback):

        already_added = True
        if not topic in self.callbacks.keys():
            self.callbacks[topic] = []
            already_added = False
        if callback in self.callbacks[topic]:
            return
        self.callbacks[topic].append(callback)
        if already_added is False:
            print topic, callback
            self.socket_sub.setsockopt(zmq.SUBSCRIBE, str(topic))

    def callback_do(self, topic, msg):
        callback_list = self.callbacks.get(topic)
        if callback_list is None:
            return
        for callback in callback_list:
            callback(topic, msg)

    def listen(self):
        self.poller = zmq.Poller()
        self.poller.register(self.socket_sub, zmq.POLLIN)
        socks = dict(self.poller.poll(50))
        if socks.get(self.socket_sub) is not None:
            print "got message"
            topic, msg = self.socket_sub.recv_multipart()
            self.callback_do(topic, msg)
