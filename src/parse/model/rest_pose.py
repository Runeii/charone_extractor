from dataclasses import dataclass, field
from io import BytesIO
from src.utils.binary_reader import BinaryReader
from typing import List

@dataclass
class RestPoseBoneRotation:
  x: int = field(default=0)
  y: int = field(default=0)
  z: int = field(default=0)

@dataclass
class RestPose:
  data: bytes

  offset_x: int = field(default=0)
  offset_y: int = field(default=0)
  offset_z: int = field(default=0)

  bone_rotations: List[RestPoseBoneRotation] = field(default_factory=list)
  
  def __post_init__(self):
    stream = BytesIO(self.data)

    _ = BinaryReader.read_uint16(stream) # frame count, not applicable
    bone_count = BinaryReader.read_uint16(stream)

    self.offset_x = BinaryReader.read_uint16(stream)
    self.offset_y = BinaryReader.read_uint16(stream)
    self.offset_z = BinaryReader.read_uint16(stream)

    for _ in range(bone_count):
      x = BinaryReader.read_uint16(stream)
      y = BinaryReader.read_uint16(stream)
      z = BinaryReader.read_uint16(stream)

      self.bone_rotations.append(RestPoseBoneRotation(x, y, z))
