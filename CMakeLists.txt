cmake_minimum_required(VERSION 3.0)

project(ros_protobuf_bridge)

# This CMake function invokes the ROS bridge auto generation script.
# It auto generates a ROS msg interface in C++ & Python that enables users to
# send Protobuf via ROS comms. It produces a <Proto_file>.ros.h header inside the
# "<CMAKE_BUILD_DIR>/proto_ros/cpp/<pkg_name>/" directory. This header can be included by
# ROS nodes to transport the corresponding protobufs over ROS topicsas well as log to
# ROS bags. It additionally produces a Python interface class inside
# "<CMAKE_BUILD_DIR>/proto_ros/python/<pkg_name>/msg/". This makes the protobuf inspectible
# by ROS tools such as "rostopic echo" etc.

# Usage: Function expects the filenames of the python modules produced by the Protobuf compiler (protoc).
# protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_MSGS})
# protobuf_generate_python(PROTO_PY ${PROTO_MSGS})
# # generate ROS Proto bridge
# generate_ros_proto_bridge(${PROTO_PY})
#
# Note: Make sure "<CMAKE_BUILD_DIR>/proto_ros/python" is set in your PYTHONPATH or install
# to appropriate Python package locations"
function(GENERATE_ROS_PROTO_BRIDGE)
  set(PROTOBUF_ROS_EXECUTABLE "${PROJECT_SOURCE_DIR}/gen/ProtobufROSgen.py")
  foreach(FIL ${ARGN})
    get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
    get_filename_component(FIL_WE ${FIL} NAME_WE)
    add_custom_target(ros_proto_${FIL_WE} ALL
      DEPENDS ${PROTO_PY})
    add_custom_command(
      TARGET ros_proto_${FIL_WE}
      #PRE_BUILD
      COMMAND ${PROTOBUF_ROS_EXECUTABLE}
      ARGS ${ABS_FIL}
      DEPENDS ${ABS_FIL} ${PROTOBUF_ROS_EXECUTABLE}
      COMMENT "Running protocol buffer ROS bridge generator on ${FIL}"
      VERBATIM )
  endforeach()
endfunction()


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rosbag
  std_msgs
  message_generation
  )

# Declare the message files to be built
add_message_files(FILES
  Foo.msg
  )

# Actually generate the language-specific message and service files
generate_messages(DEPENDENCIES)

find_package(Protobuf REQUIRED)
# generate protobuf
list(APPEND PROTO_MSGS "${CMAKE_CURRENT_SOURCE_DIR}/proto_msg/Bar.proto")
list(APPEND PROTO_MSGS "${CMAKE_CURRENT_SOURCE_DIR}/proto_msg/BarPlus.proto")
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_MSGS})
list(APPEND ${HDRS} ${PROTO_HDRS})
list(APPEND ${SRCS} ${PROTO_SRCS})
protobuf_generate_python(PROTO_PY ${PROTO_MSGS})

# generate ROS Proto bridge
generate_ros_proto_bridge(${PROTO_PY})
add_library(bar_proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})
target_include_directories(bar_proto PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR}/proto_ros/cpp)
target_link_libraries(bar_proto  ${PROTOBUF_LIBRARIES})

# define publisher
add_executable(pub src/pub.cpp)
add_dependencies(pub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(pub PUBLIC ${catkin_INCLUDE_DIRS} ${PROJECT_SOURCE_DIR})
target_link_libraries(pub ${catkin_LIBRARIES} bar_proto)

# define subscriber
add_executable(sub src/sub.cpp)
add_dependencies(sub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(sub PUBLIC ${catkin_INCLUDE_DIRS} ${PROJECT_SOURCE_DIR})
target_link_libraries(sub ${catkin_LIBRARIES} bar_proto)

# define bag reader
add_executable(bag_reader src/bag_reader.cpp)
add_dependencies(bag_reader ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(bag_reader PUBLIC ${catkin_INCLUDE_DIRS})
target_link_libraries(bag_reader ${catkin_LIBRARIES} bar_proto)
