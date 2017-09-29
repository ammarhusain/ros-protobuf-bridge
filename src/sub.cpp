 #include <ros_protobuf_bridge/BarPlus.ros.h>
//#include <manual-gen/BarPlus_ros.h>
#include "ros/ros.h"

// void chatterCallbackBar(const ros_protobuf_bridge::Bar &msg) {
//   ROS_INFO("I heard: [%d] with %d string", 1, msg.some_strings_size());
//   for (int i = 0; i < msg.some_strings_size(); ++i) {
//     ROS_INFO("%s", msg.some_strings(i).c_str());
//   }
// }

void chatterCallbackFooBar(const ros_protobuf_bridge::BarPlus &msg) {
    ROS_INFO("I heard: [%d] with %d string", 1, msg.b().some_strings_size());
    //return chatterCallbackBar(msg.b());
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallbackFooBar);
  ros::spin();

  return 0;
}
