from dataclasses import dataclass, field
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
  data: bytes

  parent_bone: int = field(init=None)
  bone_length: int = field(init=None)
  unknown1: int = field(init=None)
  unknown2: int = field(init=None)
  unknown_data: bytes = field(init=None)

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]
      
  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  @staticmethod
  def read_int16(stream: BytesIO) -> int:
    return struct.unpack("<h", stream.read(2))[0]

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.parent_bone = self.read_int16(stream)

    self.unknown1 = self.read_uint16(stream)
    self.unknown2 = self.read_uint32(stream)
    
    self.bone_length = self.read_int16(stream) # wiki incorrectly states this is uint16

    self.unknown_data = stream.read(54)

  def __repr__(self):
      return f"Bone(parent={self.parent_bone}, length={self.bone_length}, unknown_data={self.unknown_data})"