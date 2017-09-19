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
class @Class@(genpy.Message):
  _md5sum = "@Checksum@"
  _type = "@Package@/@Class@"
  _has_header = False
  _full_text = "Protobuf generated msg for @Package@::@Class@"
  __slots__ = ['@Class@']
  _slot_types = ['@Class@']

  def __init__(self, *args, **kwds):
    self.@Class@ = @PROTO_PY@.@Class@()
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
      self.@Class@ = @PROTO_PY@.@Class@()
      self.@Class@.ParseFromString(str)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # Most likely buffer underfill

  def serialize_numpy(self, buff, numpy):
    self.serialize(buff)

  def deserialize_numpy(self, str, numpy):
    self.deserialize(str)
    return self
    """
    py = py.replace("@PROTO_PY@", proto_file_name + "_pb2")
    py = py.replace("@Checksum@", checksum)
    py = py.replace("@Class@", class_name)
    py = py.replace("@Package@", pkg_name)
    s.write(py)


def GeneratePyHeader(proto_file_name, pkg_name, class_names):
    """
    Umbrella function that generates the entire header implementing ROS msg traits
    :return:
    """
    s = StringIO()
    py = """
#! /usr/bin/python

import @PROTO_PY@
import sys
import genpy
import struct
python3 = True if sys.hexversion > 0x03000000 else False
    """
    py = py.replace("@PROTO_PY@", proto_file_name + "_pb2")
    s.write(py);

    for c in class_names:
        WritePyClass(s, proto_file_name, pkg_name, c)

    py_header = s.getvalue()
    s.close()
    return py_header
