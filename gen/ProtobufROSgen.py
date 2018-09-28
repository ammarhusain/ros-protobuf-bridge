#!/usr/bin/env python

import sys
import ntpath
import os
import imp
from ProtobufROScpp import generate_cpp_header
from ProtobufROSpy import generate_py_header
try:
    from cStringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO  # Python 3.x

def throw_compilation_error(error_string):
    """
    :param error_string:
    :return:
    """
    sys.exit("{0}:1:error ProtobufROSgen: {1}\n".format(sys.argv[1], error_string))

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def write_to_file(file_name, file_data):
    with open(file_name, 'w') as f:
        f.write(file_data)



"""
Main routine
This Python script auto generates a ROS msg interface in C++ & Python that enables users to
send Protobuf via ROS comms. It produces a <Proto_file>.ros.h header inside the
'<CMAKE_BUILD_DIR>/proto_ros/cpp/<pkg_name>/' directory. This header can be included by
ROS nodes to transport the corresponding protobufs over ROS topicsas well as log to
ROS bags. It additionally produces a Python interface class inside
'<CMAKE_BUILD_DIR>/proto_ros/python/<pkg_name>/msg/'. This makes the protobuf inspectible
by ROS tools such as "rostopic echo" etc.

Note: Make sure '<CMAKE_BUILD_DIR>/proto_ros/python' is set in your PYTHONPATH or install
to appropriate Python package locations"
"""

if __name__ == '__main__':
    # get the filename from arguments
    if (len(sys.argv) == 1):
        print("[ProtobufROSgen] Usage: ./ProtobufROSgen.py <file_name>.proto")
    else:
        proto_file = sys.argv[1]
        # optional second argument for output directory
        out_dir = "./"
        if len(sys.argv) == 3:
            out_dir = sys.argv[2] + "/"
        file_w_extension = ntpath.basename(proto_file)
        proto_file_name = ntpath.splitext(file_w_extension)[0]
        proto_dir = ntpath.dirname(proto_file)
        # Add the protobuf output headers to sys paths for future imports
        sys.path.append(proto_dir)
        mod = imp.load_source('DESCRIPTOR', proto_file)
        # extract the package names: . is the delimiter in proto syntax
        pkg_name = mod.DESCRIPTOR.package
        if pkg_name.find(".") != -1:
            throw_compilation_error("(Marble: Protobuf ROS bridge) Nested Protobuf package names are not supported for ROS header code generation: %s"%pkg_name)

        class_names = list(mod.DESCRIPTOR.message_types_by_name)
        proto_file_name = proto_file_name.replace("_pb2", "")

        # write out the generated header in the pkg_name directory
        py_pkg_dir = '%s/proto_ros/python/%s' %(out_dir, pkg_name)
        create_directory('%s/msg' %py_pkg_dir)
        # write out __init__ files.
        s = StringIO()
        init_file = '%s/__init__.py'%py_pkg_dir
        write_to_file(init_file, s.getvalue())
        init_file = '%s/msg/__init__.py'%py_pkg_dir
        s.write('from .%s import *\n'%proto_file_name)
        with open(init_file, 'a') as f:
            f.write(s.getvalue())
        s.close()

        py_header = generate_py_header(proto_file_name, pkg_name, class_names)
        py_header_file = '%s/msg/%s.py' %(py_pkg_dir, proto_file_name)
        write_to_file(py_header_file, py_header)

        # create a cpp header
        cpp_pkg_dir = '%s/proto_ros/cpp/%s' %(out_dir, pkg_name)
        create_directory(cpp_pkg_dir)
        cpp_header = generate_cpp_header(proto_file_name, pkg_name, class_names)
        cpp_header_file = '%s/%s.ros.h' %(cpp_pkg_dir, proto_file_name)
        write_to_file(cpp_header_file, cpp_header)
