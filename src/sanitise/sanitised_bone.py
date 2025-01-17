from dataclasses import dataclass, field
from typing import List
from io import BytesIO
import struct
from ..parse.model.bone import Bone

@dataclass
class SanitisedBone:
  """ A bone with unknown data decomposed into known values.

  - transform_matrix (48 bytes): 3x4 matrix of floats
  - extra_data (6 bytes): 3 shorts
  """
  bone: Bone

  parent_bone: int = field(init=False)

  transform_matrix: List[List[float]] = field(init=False)
  extra_data: List[int] = field(init=False)

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]

  @staticmethod
  def read_int16(stream: BytesIO) -> int:
    return struct.unpack("<h", stream.read(2))[0]

  def __post_init__(self):
    self.parent_bone = self.bone.parent_bone - 1
    self.deconstruct_unknown_data(self.bone.unknown_data)

  def sanitise_parent_bone(self):
    self.parent_bone = self.parent_bone - 1
  
  def deconstruct_unknown_data(self, data: bytes):
    stream = BytesIO(data)

    # Extract 3x4 transform matrix (48 bytes)
    self.transform_matrix = []
    for row in range(3):
      matrix_row = []
      for col in range(4):
        value = self.read_uint32(stream)
        float_val = value / 4096.0  # Fixed point conversion
        matrix_row.append(float_val)
      self.transform_matrix.append(matrix_row)
  
    # Remaining 6 bytes as 3 shorts
    self.extra_data = []
    for _ in range(3):
        value = self.read_int16(stream)
        self.extra_data.append(value)

  def __repr__(self):
      return f"Bone(parent={self.parent_bone}, length={self.bone_length}, unknown_data={self.unknown_data})"