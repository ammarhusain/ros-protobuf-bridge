#!/usr/bin/env python

import sys
import ntpath
import os
from ProtobufROScpp import GenerateCppHeader
from ProtobufROSpy import GeneratePyHeader
try:
    from cStringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO  # Python 3.x

def ThrowCompilationError(error_string):
    """
    :param error_string:
    :return:
    """
    sys.exit("{0}:1:error Protobuf_ROSmsgGen: {1}\n".format(sys.argv[1], error_string))

def CreateDirectory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def WriteToFile(file_name, file_data):
    with open(file_name, 'w') as f:
        f.write(file_data)


################################################
# Main routine
################################################
if __name__ == '__main__':

    # get the filename from arguments
    if (len(sys.argv) == 1):
        print("[Protobuf_ROSmsgGen] Usage: ./Protobuf_ROSmsgGen.py <file_name>.proto")
    else:
        proto_file = sys.argv[1]
        file_w_extension = ntpath.basename(proto_file)
        proto_file_name = ntpath.splitext(file_w_extension)[0]
        mod = __import__("%s"%proto_file_name)
        # extract the package names: . is the delimiter in proto syntax
        pkg_name = mod.DESCRIPTOR.package
        if pkg_name.find(".") != -1:
            ThrowCompilationError("Nested Protobuf package names are not supported with the ROS bridge: %s"%pkg_name)

        class_names = list(mod.DESCRIPTOR.message_types_by_name)
        proto_file_name = proto_file_name.replace("_pb2", "")

        # write out the generated header in the pkg_name directory
        py_pkg_dir = 'proto_ros/python/%s' %pkg_name
        CreateDirectory('%s/msg' %py_pkg_dir)
        # write out __init__ files.
        s = StringIO()
        init_file = '%s/__init__.py'%py_pkg_dir
        WriteToFile(init_file, s.getvalue())
        init_file = '%s/msg/__init__.py'%py_pkg_dir
        s.write('from .%s import *\n'%proto_file_name)
        with open(init_file, 'a') as f:
            f.write(s.getvalue())
        s.close()

        py_header = GeneratePyHeader(proto_file_name, pkg_name, class_names)
        py_header_file = '%s/msg/%s.py' %(py_pkg_dir, proto_file_name)
        WriteToFile(py_header_file, py_header)

        # create a cpp header
        cpp_pkg_dir = 'proto_ros/cpp/%s' %pkg_name
        CreateDirectory(cpp_pkg_dir)
        cpp_header = GenerateCppHeader(proto_file_name, pkg_name, class_names)
        cpp_header_file = '%s/%s.ros.h' %(cpp_pkg_dir, proto_file_name)
        WriteToFile(cpp_header_file, cpp_header)
