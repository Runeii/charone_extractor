from dataclasses import dataclass, field
from io import BytesIO
from ....utils.binary_reader import BinaryReader

@dataclass
class Pose:
  data: bytes

  byte1: int = field(init=0)
  byte2: int = field(init=0)
  byte3: int = field(init=0)
  byte4: int = field(init=0)
  
  def __post_init__(self):
    assert len(self.data) == 4, f"Pose data must be 4 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.byte1 = BinaryReader.read_int8(stream)
    self.byte2 = BinaryReader.read_int8(stream)
    self.byte3 = BinaryReader.read_int8(stream)
    self.byte4 = BinaryReader.read_int8(stream)

  @staticmethod
  def calculate_size():
    return 4