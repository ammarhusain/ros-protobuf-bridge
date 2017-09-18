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
        file = open(proto_file, "r")
        proto_schema = file.read()
        entries = re.split("[\r\n;]+", proto_schema)
        res = ("package" in e for e in entries)
        pkg_x = [x.split()[1] for x in entries if "package" in x]
        # make sure that package name exists
        if (len(pkg_x) != 1):
            ThrowCompilationError("Must specify a package name")
        pkg_name = pkg_x[0]
        # make sure its not a nested package name ... Not supported for now
        if [dot for dot in pkg_name if "." in dot]:
            ThrowCompilationError("Nested package names not supported")
        # now get all the class names
        class_names = [x.split()[1] for x in entries if "message" in x]

        # create a cpp header
        GenerateCppHeader(proto_file_name, pkg_name, class_names)
        GeneratePyHeader(proto_file_name, pkg_name, class_names)
