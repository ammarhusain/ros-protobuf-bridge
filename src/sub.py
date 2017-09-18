#!/usr/bin/env python
import rospy
from ros_protobuf_bridge.msg import BarPlus

def callback(data):
    print data
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.b.kv.val)

def listener():
    rospy.init_node('py_listener', anonymous=True)
    rospy.Subscriber("chatter", BarPlus, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
