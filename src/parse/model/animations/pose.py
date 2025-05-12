from dataclasses import dataclass, field
from io import BytesIO
from src.utils.binary_reader import BinaryReader

@dataclass
class Pose:
  data: bytes

  byte1: int = field(default=0)
  byte2: int = field(default=0)
  byte3: int = field(default=0)
  byte4: int = field(default=0)
  
  def __post_init__(self):
    assert len(self.data) == 4, f"Pose data must be 4 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.byte1 = BinaryReader.read_uint8(stream)
    self.byte2 = BinaryReader.read_uint8(stream)
    self.byte3 = BinaryReader.read_uint8(stream)
    self.byte4 = BinaryReader.read_uint8(stream)

  @staticmethod
  def calculate_size():
    return 4