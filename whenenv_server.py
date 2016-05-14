import zmq
import uuid
import time
import json

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)


socket_pub = context.socket(zmq.PUB)

socket_sub.bind("tcp://127.0.0.1:5000")


socket_pub.bind("tcp://127.0.0.1:5001")

process_id = uuid.uuid4()

clients = {}

topics = {}

def register(msg):
    print "register=%s" % (msg)
    msg = json.loads(msg)
    output = {
        'master' : str(process_id),
        'topics' : {}
        }
    for topic in msg["topics"]:
        topic_id = topics.get(topic)
        if topic_id is None:
            topic_id = str(uuid.uuid4())
            topics[topic] = topic_id
        output['topics'][topic] = topic_id
    socket_pub.send_multipart([str(msg['identity']), str(json.dumps(output))])


def process(msg):
    print "process=%s" % (msg)

knownchannles = {
    "c2a4d156-114b-4ad8-ae87-cfa14b261bde" : register,
    }


for key in knownchannles.keys():
    socket_sub.setsockopt(zmq.SUBSCRIBE, key)
poller = zmq.Poller()
poller.register(socket_sub, zmq.POLLIN)
#poller.register(socket_pub, zmq.POLLIN)

while True:
    socks = dict(poller.poll(50))
    if socks.get(socket_sub) is not None:
        print "got message"
        topic, msg = socket_sub.recv_multipart()
        handler = knownchannles.get(topic)
        handler(msg)
    if socks.get(socket_pub) is not None:
        print "has message to send"
    for key in topics.keys():
        print key
        print topics.get(key)
        socket_pub.send_multipart([str(topics.get(key)), str("dddd")])
