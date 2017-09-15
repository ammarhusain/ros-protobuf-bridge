cmake_minimum_required(VERSION 3.0)

project(ros_protobuf_bridge)

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
  message("using protoc: ${PROTOBUF_PROTOC_EXECUTABLE}")
  protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${CMAKE_CURRENT_SOURCE_DIR}/proto/Bar.proto)
  protobuf_generate_python(PROTO_PY ${CMAKE_CURRENT_SOURCE_DIR}/proto/Bar.proto)
  message("proto py: ${PROTO_PY}")
  add_library(bar_proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})

  # define executable using MyMessage1 etc.
  add_executable(pub src/pub.cpp)
  add_dependencies(pub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
  target_include_directories(pub PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(pub ${catkin_LIBRARIES})

  # define executable using MyMessage1 etc.
  add_executable(sub src/sub.cpp)
  add_dependencies(sub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
  target_include_directories(sub PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(sub ${catkin_LIBRARIES})


  target_include_directories(pub PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(pub ${PROTOBUF_LIBRARIES} bar_proto)

  target_include_directories(sub PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(sub ${PROTOBUF_LIBRARIES} bar_proto)
