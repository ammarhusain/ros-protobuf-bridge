#include "ros/ros.h"
#include <ros_protobuf_bridge/BarPlus.ros.h>
// #include <manual-gen/BarPlus_ros.h>

#include <string>

/// Foo publisher.
int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");

  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<ros_protobuf_bridge::BarPlus>("chatter", 1000);

  ros::Rate loop_rate(10);

  ros_protobuf_bridge::BarPlus prot;

  int count = 0;
  while (ros::ok())
  {
    // prot.set_page_number(count);
    for (int i = 0; i < count; i++) {
      prot.mutable_b()->add_some_strings("foo_string");
    }
    prot.mutable_b()->mutable_kv()->set_val(10);
    chatter_pub.publish(prot);

    ROS_INFO("str sz: %d", prot.mutable_b()->some_strings_size());
    prot.mutable_b()->clear_some_strings();
    ros::spinOnce();
    loop_rate.sleep();
    ++count;
    count = count % 15;
  }


  return 0;
}
