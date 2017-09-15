cmake_minimum_required(VERSION 3.0)

project(ros_protobuf_bridge)

function(GENERATE_ROS_PROTO_BRIDGE HDRS)
  set(PROTOBUF_ROS_EXECUTABLE "${PROJECT_SOURCE_DIR}/gen/Protobuf_ROSmsgGen.py")
  foreach(FIL ${ARGN})
    get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
    get_filename_component(FIL_WE ${FIL} NAME_WE)
    list(APPEND ${HDRS} "${CMAKE_CURRENT_BINARY_DIR}/${FIL_WE}.ros.h")
    add_custom_command(
      OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/${FIL_WE}.ros.h"
      COMMAND  ${PROTOBUF_ROS_EXECUTABLE}
      ARGS ${ABS_FIL}
      DEPENDS ${ABS_FIL} ${PROTOBUF_ROS_EXECUTABLE}
      COMMENT "Running protocol buffer ROS bridge generator on ${FIL}"
      VERBATIM )
    add_custom_target(ros_proto_${FIL_WE}
      ALL
      DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/${FIL_WE}.ros.h"
      COMMENT "Checking if ROS Proto bridge regeneration required for: ${FIL}")
  endforeach()

  set_source_files_properties(${${HDRS}} PROPERTIES GENERATED TRUE)
  set(${HDRS} ${${HDRS}} PARENT_SCOPE)
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
  message("using protoc: ${PROTOBUF_PROTOC_EXECUTABLE}")
  protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${CMAKE_CURRENT_SOURCE_DIR}/proto/Bar.proto)
  protobuf_generate_python(PROTO_PY ${CMAKE_CURRENT_SOURCE_DIR}/proto/Bar.proto)

  # generate ROS Proto bridge
  generate_ros_proto_bridge(ROS_HDRS ${CMAKE_CURRENT_SOURCE_DIR}/proto/Bar.proto)
  message("ros bridge hdrs: ${ROS_HDRS}")
  message("proto py: ${PROTO_PY}")

  add_library(bar_proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})

  # define publisher
  add_executable(pub src/pub.cpp)
  add_dependencies(pub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
  target_include_directories(pub PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(pub ${catkin_LIBRARIES})

  # define subscriber
  add_executable(sub src/sub.cpp)
  add_dependencies(sub ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
  target_include_directories(sub PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(sub ${catkin_LIBRARIES})


  target_include_directories(pub PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(pub ${PROTOBUF_LIBRARIES} bar_proto)

  target_include_directories(sub PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(sub ${PROTOBUF_LIBRARIES} bar_proto)


  # define bag reader
  add_executable(bag_reader src/bag_reader.cpp)
  add_dependencies(bag_reader ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
  target_include_directories(bag_reader PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(bag_reader ${catkin_LIBRARIES})

  target_include_directories(bag_reader PUBLIC ${PROTOBUF_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
  target_link_libraries(bag_reader ${PROTOBUF_LIBRARIES} bar_proto)
