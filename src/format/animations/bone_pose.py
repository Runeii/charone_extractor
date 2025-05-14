from dataclasses import dataclass
from src.parse.model.animations.pose import Pose
from math import pi

@dataclass(init=False)
class BonePose:
  x: float
  y: float
  z: float

  def __init__(self, original: Pose):
    raw_x = self.decode_rotation(original.byte2, 0b00001100, original.byte4, 6)
    raw_y = self.decode_rotation(original.byte3, 0b00110000, original.byte4, 4)
    raw_z = self.decode_rotation(original.byte1, 0b00000011, original.byte4, 8)

    # Convert to radians using decimal values
    self.x = pi * raw_x / 2048
    self.y = pi * raw_y / 2048
    self.z = pi * raw_z / 2048
    
  def decode_rotation(self, low_byte: int, high_byte_mask: int, high_byte: int, shift: int) -> int:
    # Combine the low byte with masked & shifted high byte
    high_bits = (high_byte & high_byte_mask) << shift
    combined = (low_byte | high_bits) << 2
    
    # Handle negative numbers (signed 12-bit conversion)
    if combined >= 2048:
        combined -= 4096
    return combined