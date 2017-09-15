import rosbag
from ros_protobuf_bridge.msg import Bar
print 'starting'
bag = rosbag.Bag('test.bag')
print 'bag loaded'
for topic, msg, t in bag.read_messages(topics=['/chatter'], raw=True):
    b = Bar()
    print Bar.deserialize(b, msg[1])
bag.close()
