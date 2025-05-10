from dataclasses import dataclass
from src.parse.model.animations.pose import Pose
from math import pi

@dataclass(init=False)
class BonePose:
  x: float
  y: float
  z: float

  def __init__(self, original: Pose):
    # Get raw values
    raw_x = decode_rotation(original.byte2, 0x0C, original.byte4, 6)  # mask 0x0C = 0b00001100
    raw_z = decode_rotation(original.byte1, 0x03, original.byte4, 8)  # mask 0x03 = 0b00000011
    raw_y = decode_rotation(original.byte3, 0x30, original.byte4, 4)  # mask 0x30 = 0b00110000
    
    # Convert to radians
    self.x = pi * raw_x / 0x800
    self.y = pi * raw_y / 0x800
    self.z = pi * raw_z / 0x800


def decode_rotation(low_byte: int, high_byte_mask: int, high_byte: int, shift: int) -> int:
    # Combine the low byte with masked & shifted high byte
    high_bits = (high_byte & high_byte_mask) << shift
    combined = (low_byte | high_bits) << 2
    
    # Handle negative numbers (signed 12-bit conversion)
    if combined >= 0x800:
        combined -= 0x1000
    return combined