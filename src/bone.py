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
  - unknown_data (60 bytes): 15 DWORDs - unknown values
  """
  parent_bone: int
  bone_length: int
  unknown1: int
  unknown2: int
  unknown_data: List[int]  # 15 DWORDs of unknown data

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

    # Read parent bone ID (convert from 1-based to 0-based)
    self.parent_bone = self.read_int16(stream) - 1
    
    self.unknown1 = self.read_uint16(stream)
    self.unknown2 = self.read_uint32(stream)
    
    # Read bone length with special handling for negative values
    bone_length = self.read_uint16(stream)
    if bone_length > 0x8000:
        bone_length -= 0x10000
    self.bone_length = bone_length

    # Read remaining unknown DWORDs
    self.unknown_data = [
        self.read_uint32(stream) for _ in range(13)  # 13 instead of 15 since we already read 10 bytes
    ]

  def __repr__(self):
      return f"Bone(parent={self.parent_bone}, length={self.bone_length})"