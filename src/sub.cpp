#include "ros/ros.h"
#include "ros_protobuf_bridge/Foo.h"
#include "Bar_ros.h"

void chatterCallback(const ros_protobuf_bridge::Foo& msg)
{
  ROS_INFO("I heard: [%d]", msg.a);
}

void chatterCallbackBar(const ros_protobuf_bridge::Bar& msg)
{
  ROS_INFO("I heard: [%d] with %d string", msg.page_number(), msg.some_strings_size());
  for (int i = 0; i < msg.some_strings_size(); ++i) {
    ROS_INFO("%s", msg.some_strings(i).c_str());
  }
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallbackBar);
  ros::spin();

  return 0;
}
