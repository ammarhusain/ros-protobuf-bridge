#pragma once

#include "Bar.pb.h"

#include <ros/message_traits.h>
#include <ros/serialization.h>

namespace ros {
namespace message_traits {

template <>
struct MD5Sum<ros_protobuf_bridge::Bar> {
  static const char* value(ros_protobuf_bridge::Bar const& o) {
    return "003ab2255988927d7e6b13ccbf717699";
  }
  static const char* value() {
    return "003ab2255988927d7e6b13ccbf717699";
  }
};

template <>
struct DataType<ros_protobuf_bridge::Bar> {
  static const char* value(ros_protobuf_bridge::Bar const& o) {
    return "ros_protobuf_bridge/Bar";
  }
  static const char* value() {
    return "ros_protobuf_bridge/Bar";
  }
};

template <>
struct Definition<ros_protobuf_bridge::Bar> {
  static const char* value(ros_protobuf_bridge::Bar const& o) {
    return "ros_protobuf_bridge::Bar is not a traditional ROS msg and is not defined in the ROS message IDL, "
           "though would look something like uint8[] serialized_data";
  }
  static const char* value() {
    return "ros_protobuf_bridge::Bar is not a traditional ROS msg and is not defined in the ROS message IDL, "
           "though would look something like uint8[] serialized_data";
  }
};
}  // namespace message_traits

namespace serialization {
template <>
struct Serializer<ros_protobuf_bridge::Bar> {
  template <typename Stream>
  inline static void write(Stream& stream, ros_protobuf_bridge::Bar const& o) {
    std::string ser_bytes;
    if (!o.SerializeToString(&ser_bytes)) {
      std::cerr << "Serialization failed." << std::endl;
      return;
    }
    memcpy(stream.advance(ser_bytes.size()), ser_bytes.c_str(), ser_bytes.size());
  }

  template <typename Stream>
  inline static void read(Stream &stream, ros_protobuf_bridge::Bar &o) {
    std::string deser_bytes;
    deser_bytes.resize(stream.getLength());
    memcpy(&deser_bytes[0], stream.advance(stream.getLength()),
           stream.getLength());
    if (!o.ParseFromString(deser_bytes)) {
      std::cerr << "Deserialization failed." << std::endl;
      return;
    }
  }

  inline static uint32_t
  serializedLength(ros_protobuf_bridge::Bar const &o) {
    return o.ByteSizeLong();
  }
};
}  // namespace serialization

}  // namespace ros
