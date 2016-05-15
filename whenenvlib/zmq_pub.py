import zmq

class zmq_pub:
    def __init__(self, **kwargs):

        context = zmq.Context()
        self.socket_pub = context.socket(zmq.PUB)

        self.addr = kwargs.get('addr', None)

        self.socket_pub.bind(self.addr)

        self.process_id = kwargs.get('process_id', None)

        self.clients = {}

        self.topics = {}


    def send_multipart(self, topic, msg):
        self.socket_pub.send_multipart([topic, msg])
