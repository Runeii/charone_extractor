import struct
from dataclasses import dataclass, field
from io import BytesIO
from typing import List
from ...binary_reader import BinaryReader

@dataclass
class AnimationsHeader:
  data: bytes
  number_of_animations: int = field(init=False)
  number_of_frames: int = field(init=False)
  bone_count: int = field(init=False)
  coordinate_offset: List[int] = field(init=False)

  def __post_init__(self):
    stream = BytesIO(self.data)

    self.number_of_animations = BinaryReader.read_uint16(stream)
    self.number_of_frames = BinaryReader.read_uint16(stream)
    self.bone_count = BinaryReader.read_uint16(stream)

    self.coordinate_offset = [
      BinaryReader.read_uint16(stream),
      BinaryReader.read_uint16(stream),
      BinaryReader.read_uint16(stream)
    ]