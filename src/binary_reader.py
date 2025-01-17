import struct
from dataclasses import dataclass, field
from io import BytesIO

class BinaryReader:
  @staticmethod
  def read_uint8(stream: BytesIO) -> int:
    return struct.unpack("<B", stream.read(1))[0]
  
  @staticmethod
  def read_int8(stream: BytesIO) -> int:
    return struct.unpack("<b", stream.read(1))[0]

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  @staticmethod
  def read_int16(stream: BytesIO) -> int:
    return struct.unpack("<h", stream.read(2))[0]

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]

  @staticmethod
  def read_int32(stream: BytesIO) -> int:
    return struct.unpack("<i", stream.read(4))[0]
  
  @staticmethod
  def read_string(stream: BytesIO, length: int = 8) -> str:
    raw_str = stream.read(length)
    return raw_str.split(b'\x00')[0].decode('ascii', errors='ignore')