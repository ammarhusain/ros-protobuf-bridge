#include <algorithm>
#include <boost/foreach.hpp>
#include <ros_protobuf_bridge_init/Bar.ros.h>
#include <rosbag/bag.h>
#include <rosbag/view.h>
#define foreach BOOST_FOREACH

int main() {

  rosbag::Bag bag;
  bag.open("/home/ammar/src/ros-protobuf-bridge/src/test.bag",
           rosbag::bagmode::Read);

  std::vector<std::string> topics;
  topics.push_back(std::string("/chatter"));
  rosbag::View view(bag, rosbag::TopicQuery(topics));
  foreach (rosbag::MessageInstance const m, view) {
    boost::shared_ptr<ros_protobuf_bridge_init::Bar> s =
        m.instantiate<ros_protobuf_bridge_init::Bar>();
    if (s != NULL) {
      std::cout << s->some_strings_size() << std::endl;
      for (int i = 0; i < s->some_strings_size(); ++i) {
        std::cout << s->some_strings(i) << std::endl;
      }
    }
  }

  bag.close();

  return 0;
}
