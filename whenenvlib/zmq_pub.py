import zmq

class zmq_pub:
    def __init__(self, **kwargs):
        self.zmq_context = kwargs.get('zmq_context', None)
        if self.zmq_context is None:
            self.zmq_context = zmq.Context()

        self.socket_pub = self.zmq_context.socket(zmq.PUB)

        self.addr = kwargs.get('addr', None)

        self.socket_pub.bind(self.addr)

        self.process_id = kwargs.get('process_id', None)

        self.clients = {}

        self.topics = {}


    def send_multipart(self, topic, msg):
        self.socket_pub.send_multipart([topic, msg])
