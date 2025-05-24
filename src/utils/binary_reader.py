import struct
from io import BytesIO

class BinaryReader:
  @staticmethod
  def read_uint8(stream: BytesIO) -> int:
    return struct.unpack("<B", stream.read(1))[0]

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]
  
  @staticmethod
  def read_bytes(stream: BytesIO, length: int) -> bytes:
    return stream.read(length)