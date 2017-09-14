#include "ros/ros.h"
#include "ros_protobuf_bridge/Foo.h"
#include "Bar_ros.h"

void chatterCallback(const ros_protobuf_bridge::Foo& msg)
{
  ROS_INFO("I heard: [%d]", msg.a);
}

void chatterCallbackBar(const ros_protobuf_bridge::Bar& msg)
{
  ROS_INFO("I heard: [%d]", msg.page_number());
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallbackBar);
  ros::spin();

  return 0;
}
