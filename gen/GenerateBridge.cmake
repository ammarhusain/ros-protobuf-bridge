function(GENERATE_ROS_PROTO_BRIDGE HDRS SRCS)
  protobuf_generate_cpp(MSG_SRCS MSG_HDRS ${ARGN})
  list(APPEND ${HDRS} ${MSG_HDRS})
  list(APPEND ${SRCS} ${MSG_SRCS})
  protobuf_generate_python(PROTO_PY ${ARGN})
  set(PROTOBUF_ROS_EXECUTABLE "${PROJECT_SOURCE_DIR}/gen/Protobuf_ROSmsgGen.py")
  foreach(FIL ${ARGN})
    get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
    get_filename_component(FIL_WE ${FIL} NAME_WE)
    set (CPP_HDR "${CMAKE_CURRENT_BINARY_DIR}/proto_ros/cpp/${FIL_WE}.ros.h")
    list(APPEND ${HDRS} ${CPP_HDR})
    add_custom_command(
      OUTPUT ${CPP_HDR}
      COMMAND  ${PROTOBUF_ROS_EXECUTABLE}
      ARGS ${ABS_FIL}
      DEPENDS ${ABS_FIL} ${PROTOBUF_ROS_EXECUTABLE}
      COMMENT "Running protocol buffer ROS bridge generator on ${FIL}"
      VERBATIM )
    add_custom_target(ros_proto_${FIL_WE}
      ALL
      DEPENDS ${CPP_HDR}
      COMMENT "Checking if ROS Proto bridge regeneration required for: ${FIL}")
  endforeach()

  set_source_files_properties(${${SRCS}} ${${HDRS}} PROPERTIES GENERATED TRUE)
  set(${SRCS} ${${SRCS}} PARENT_SCOPE)
  set(${HDRS} ${${HDRS}} PARENT_SCOPE)
endfunction()
