from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO
import struct

@dataclass
class Bone:
  """A bone in the MCH format (64 bytes total).
  
  Structure:
  - parent_bone (2 bytes): SHORT - parent bone ID (1-based, -1 if no parent)
  - unknown1 (2 bytes): SHORT - unknown value
  - unknown2 (4 bytes): DWORD - unknown value
  - bone_length (2 bytes): SHORT - length of bone (needs special handling for negative values)
  - unknown_data (54 bytes): 54 bytes - unknown values
  """
  parent_bone: int
  bone_length: int
  unknown1: int
  unknown2: int
  unknown_data: bytes

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]
      
  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  @staticmethod
  def read_int16(stream: BytesIO) -> int:
    return struct.unpack("<h", stream.read(2))[0]

  def __init__(self, data: bytes):
    assert len(data) == 64, f"Bone must be 64 bytes, got {len(data)}"
    stream = BytesIO(data)

    self.parent_bone = self.read_int16(stream)

    self.unknown1 = self.read_uint16(stream)
    self.unknown2 = self.read_uint32(stream)
    
    self.bone_length = self.read_int16(stream) # wiki incorrectly states this is uint16

    self.unknown_data = stream.read(54)

  def __repr__(self):
      return f"Bone(parent={self.parent_bone}, length={self.bone_length}, unknown_data={self.unknown_data})"