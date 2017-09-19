#!/usr/bin/env python

import sys
import ntpath
import os
import re
import hashlib
from ProtobufROScpp import GenerateCppHeader
from ProtobufROSpy import GeneratePyHeader

def ThrowCompilationError(error_string):
    """
    :param error_string:
    :return:
    """
    sys.exit("{0}:1:error Protobuf_ROSmsgGen: {1}\n".format(sys.argv[1], error_string))

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
        pkg_name = mod.DESCRIPTOR.package
        class_names = list(mod.DESCRIPTOR.message_types_by_name)

        GeneratePyHeader(proto_file_name.replace("_pb2", ""), pkg_name, class_names)
        # create a cpp header
        GenerateCppHeader(proto_file_name.replace("_pb2", ""), pkg_name, class_names)
