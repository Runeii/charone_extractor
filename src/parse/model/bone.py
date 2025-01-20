from dataclasses import dataclass, field
from io import BytesIO
from ...utils.binary_reader import BinaryReader

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

  parent_bone: int = field(init=False)
  bone_length: int = field(init=False)
  parent_bone_offset: int = field(init=False) # wiki needs update: this is parent bone offset! (so multiple of 64)
  unknown2: int = field(init=False) # always 0x0 / 0?
  unknown_data: bytes = field(init=False)

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    
    stream = BytesIO(self.data)

    self.parent_bone = BinaryReader.read_int16(stream)

    self.parent_bone_offset = BinaryReader.read_uint16(stream)
    self.unknown2 = BinaryReader.read_uint32(stream)
    
    self.bone_length = BinaryReader.read_int16(stream) # wiki incorrectly states this is uint16

    self.unknown_data = stream.read()

  def __repr__(self):
      return f"Bone(parent={self.parent_bone}, length={self.bone_length}, unknown_data={self.unknown_data})"