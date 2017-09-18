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

def WritePyClass(s, proto_file_name, pkg_name, class_name):
    checksum = hashlib.md5("%s::%s" %(pkg_name, class_name)).hexdigest()
    py = """
#! /usr/bin/python

import @PROTO_PY@_pb2
import sys
import genpy
import struct
python3 = True if sys.hexversion > 0x03000000 else False

class @Class@(genpy.Message):
  _md5sum = "@Checksum@"
  _type = "@Package@/@Class@"
  _has_header = False
  _full_text = "Protobuf generated msg for @Package@::@Class@"
  __slots__ = ['@Class@']
  _slot_types = ['@Class@']

  def __init__(self, *args, **kwds):
    self.@Class@ = @Class@_pb2.@Class@()
  def _get_types(self):
    return self._slot_types

  def serialize(self, buff):
    try:
      buff = self.@Class@.SerializeToString()
    except struct.error as se:
      self._check_types(
          struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get(
              '_x', self)))))
    except TypeError as te:
      self._check_types(
          ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get(
              '_x', self)))))

  def deserialize(self, str):
    try:
      self.@Class@ = @Class@_pb2.@Class@()
      self.@Class@.ParseFromString(str)
      print 'deserialized @Class@: %s'%str
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # Most likely buffer underfill

  def serialize_numpy(self, buff, numpy):
    self.serialize(buff)

  def deserialize_numpy(self, str, numpy):
    self.deserialize(str)
    return self
    """
    py = py.replace("@PROTO_PY@", proto_file_name)
    py = py.replace("@Checksum@", checksum)
    py = py.replace("@Class@", class_name)
    py = py.replace("@Package@", pkg_name)
    s.write(py)


def GeneratePyHeader(proto_file_name, pkg_name, class_names):
    """
    Umbrella function that generates the entire header implementing ROS msg traits
    :return:
    """
    # write out the generated header in the pkg_name directory for include namespacing
    if not os.path.exists('proto_ros/python/%s/msg' %pkg_name):
        os.makedirs('proto_ros/python/%s/msg' %pkg_name)
    # write out __init__ files.
    s = StringIO()
    init_file = 'proto_ros/python/%s/__init__.py'%pkg_name
    with open(init_file, 'w') as f:
        f.write(s.getvalue())
    init_file = 'proto_ros/python/%s/msg/__init__.py'%pkg_name
    for c in class_names:
        s.write('from .%s import *\n'%c)
    with open(init_file, 'w') as f:
        f.write(s.getvalue())

    for c in class_names:
        s = StringIO()
        print c
        WritePyClass(s, proto_file_name, pkg_name, c)
        # write out class in pkg_name/msg directory
        # write code-gen only if different from build artifact
        header_file_name = 'proto_ros/python/%s/msg/%s.py' %(pkg_name, c)
        is_diff = True
        if os.path.isfile(header_file_name):
            with open(header_file_name, 'r') as f:
                is_diff = f.read() != s.getvalue()
        if is_diff:
            with open(header_file_name, 'w') as f:
                f.write(s.getvalue())
        s.close()
