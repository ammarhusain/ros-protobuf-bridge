#!/usr/bin/env python

import sys
import ntpath
import os
import re
import hashlib

try:
    from cStringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO  # Python 3.x

def write_checksum_trait(s, pkg_name, class_name):
    """
    This function generates the c++ code required to specialize the checksum trait for a ROS type.
    The checksum is computed with md5sum on the string '<ProtobufPackage>::<ProtobufMessageType>'.
    """
    checksum = hashlib.md5("%s::%s" %(pkg_name, class_name)).hexdigest()
    cpp = """
    template <>
    struct MD5Sum<@Package@::@Class@> {
    static const char* value(@Package@::@Class@ const& o) {
      return "@Checksum@";
    }
    static const char* value() {
      return "@Checksum@";
    }
    };
    """
    cpp = cpp.replace("@Checksum@", checksum)
    cpp = cpp.replace("@Class@", class_name)
    cpp = cpp.replace("@Package@", pkg_name)
    s.write(cpp)

def write_data_type_trait(s, pkg_name, class_name):
    """
    This function generates the c++ code required to specialize the datatype trait for a ROS type.
    """
    cpp = """
    template <>
    struct DataType<@Package@::@Class@> {
    static const char* value(@Package@::@Class@ const& o) {
      return "@Package@/@Class@";
    }
    static const char* value() {
      return "@Package@/@Class@";
    }
    };
    """
    cpp = cpp.replace("@Class@", class_name)
    cpp = cpp.replace("@Package@", pkg_name)
    s.write(cpp)

def write_definition_trait(s, pkg_name, class_name):
    """
    This function generates the c++ code required to specialize the data definition trait for a ROS type.
    """
    cpp = """
    template <>
    struct Definition<@Package@::@Class@> {
    static const char* value(@Package@::@Class@ const& o) {
      return "Marble: Protobuf generated msg for @Package@::@Class@";
    }
    static const char* value() {
      return "Marble: Protobuf generated msg for @Package@::@Class@";
    }
    };
    """
    cpp = cpp.replace("@Class@", class_name)
    cpp = cpp.replace("@Package@", pkg_name)
    s.write(cpp)

def write_serialization_trait(s, pkg_name, class_name):
    """
    This function generates the c++ code required to specialize the serialization & deserialization trait for a ROS type.
    The serialize & deserialize functions work by transforming a ROS Stream into a std::string
    and passing it over to the Protobuf C++ class for deserializing into a Protobuf C++
    object and vice versa.
    """
    cpp = """
    namespace serialization {
    template <>
    struct Serializer<@Package@::@Class@> {
    template <typename Stream>
    inline static void write(Stream& stream, @Package@::@Class@ const& o) {
      std::string ser_bytes;
      if (!o.SerializeToString(&ser_bytes)) {
        std::cerr << "Serialization failed." << std::endl;
        return;
      }
      memcpy(stream.advance(ser_bytes.size()), ser_bytes.c_str(), ser_bytes.size());
    }

    template <typename Stream>
    inline static void read(Stream &stream, @Package@::@Class@ &o) {
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
    serializedLength(@Package@::@Class@ const &o) {
      return o.ByteSizeLong();
    }
    };
    }  // namespace serialization
    """
    cpp = cpp.replace("@Class@", class_name)
    cpp = cpp.replace("@Package@", pkg_name)
    s.write(cpp)

def write_class_traits(s, pkg_name, class_name):
    """
    This function generates all the required ROS traits for a class to be compatible with ROS comms.
    """
    s.write("namespace message_traits {\n")
    write_checksum_trait(s, pkg_name, class_name)
    write_data_type_trait(s, pkg_name, class_name)
    write_definition_trait(s, pkg_name, class_name)
    s.write("}  // namespace message_traits\n")
    write_serialization_trait(s, pkg_name, class_name)

def generate_cpp_header(proto_file_name, pkg_name, class_names):
    """
    Umbrella function that generates the entire header implementing ROS msg traits.
    This enables a user to seamlessly publish & subscribe Protobuf objects inside ROS nodes.
    :return:
    """
    s = StringIO()

    cpp = """
    /// @author    Auto-generated by ProtobufROSmsgBOT
    ///
    /// @warning  This file has been autogenerated by the build process.
    ///           Do not modify this file.
    ///
    /// @note For more information on the header auto-generation,
    /// refer to the following ROS documentation:
    /// http://wiki.ros.org/roscpp/Overview/MessagesSerializationAndAdaptingTypes
    /// http://wiki.ros.org/roscpp/Overview/MessagesTraits
    ///
    /// This auto generated header wraps a Protobuf class and provides the required functions to interoperate with ROS.
    /// It enables a user to seamlessly publish & subscribe Protobuf objects inside ROS nodes.

    #pragma once

    #include <@PROTO_H@.pb.h>
    #include <ros/message_traits.h>
    #include <ros/serialization.h>

    namespace ros {
    """
    cpp = cpp.replace("@PROTO_H@", format(proto_file_name))
    s.write(cpp)

    for c in class_names:
        write_class_traits(s, pkg_name, c)
    s.write("}  // namespace ros\n")

    cpp_header = s.getvalue()
    s.close()
    return cpp_header
