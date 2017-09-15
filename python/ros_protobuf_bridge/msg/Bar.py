#! /usr/bin/python

import Bar_pb2
import sys
import genpy
import struct
python3 = True if sys.hexversion > 0x03000000 else False

class Bar(genpy.Message):
    _md5sum = "003ab2255988927d7e6b13ccbf717699"
    _type = "ros_protobuf_bridge/Bar"
    _has_header = False
    _full_text = """ros_protobuf_bridge::Bar is not a traditional ROS msg and is not
  defined in the ROS message IDL, though would look something like uint8[]
  serialized_data
  """
    __slots__ = ['Bar']
    _slot_types = ['Bar']

    def __init__(self, *args, **kwds):
        """
    Constructor.
    """
        self.Bar = Bar_pb2.Bar()

    def _get_types(self):
        """
    internal API method
    """
        return self._slot_types

    def serialize(self, buff):
        """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
        try:
            buff = self.Bar.SerializeToString()
        except struct.error as se:
            self._check_types(
                struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get(
                    '_x', self)))))
        except TypeError as te:
            self._check_types(
                ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get(
                    '_x', self)))))

    def deserialize(self, str):
        """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
        try:
            self.Bar = Bar_pb2.Bar()
            self.Bar.ParseFromString(str)
            return self
        except struct.error as e:
            raise genpy.DeserializationError(e)  # Most likely buffer underfill

    def serialize_numpy(self, buff, numpy):
        """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
        self.serialize(buff)

    def deserialize_numpy(self, str, numpy):
        """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
        print 'Called deserialize numpy'
        self.deserialize(str)
        return self
