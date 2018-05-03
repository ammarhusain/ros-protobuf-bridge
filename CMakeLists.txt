cmake_minimum_required(VERSION 3.0)

project(ros_protobuf_bridge)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rosbag
  std_msgs
  message_generation
  )

catkin_package(
  CATKIN_DEPENDS roscpp)

# Declare the message files to be built
add_message_files(FILES
  Foo.msg
  )

# Actually generate the language-specific message and service files
#generate_messages(DEPENDENCIES)

find_package(Protobuf REQUIRED)

include(gen/GenerateBridge.cmake)

# generate ROS Proto bridge
generate_ros_proto_bridge(MSG_HDRS MSG_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/proto_msg/Bar.proto)
add_library(bar_proto STATIC ${MSG_SRCS} ${MSG_HDRS})
target_include_directories(bar_proto PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR}/proto_ros/cpp)
target_link_libraries(bar_proto  ${PROTOBUF_LIBRARIES})

# define publisher
add_executable(pub src/pub.cpp)
add_dependencies(pub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(pub PUBLIC ${catkin_INCLUDE_DIRS})
target_link_libraries(pub ${catkin_LIBRARIES} bar_proto)

# define subscriber
add_executable(sub src/sub.cpp)
add_dependencies(sub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(sub PUBLIC ${catkin_INCLUDE_DIRS})
target_link_libraries(sub ${catkin_LIBRARIES} bar_proto)

# define bag reader
add_executable(bag_reader src/bag_reader.cpp)
add_dependencies(bag_reader ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(bag_reader PUBLIC ${catkin_INCLUDE_DIRS})
target_link_libraries(bag_reader ${catkin_LIBRARIES} bar_proto)
