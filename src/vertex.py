from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO
import struct

MAX_SIZE = 4096
@dataclass
class Vertex:
  """A vertex in the MCH format.
  
  Structure:
  - x (2 bytes): SHORT - X position (scaled by 1/256)
  - y (2 bytes): SHORT - Y position (scaled by 1/256)
  - z (2 bytes): SHORT - Z position (scaled by 1/256)
  - unknown1 (2 bytes): SHORT - unknown value (skipped)
  Note: Coordinates use 16-bit values with MAX_SIZE = 4096 for negative detection
  """
  x: float
  y: float
  z: float

  @staticmethod
  def read_coord(stream: BytesIO) -> float:
    value = int.from_bytes(stream.read(2), byteorder='little')
    if value > 65536 - MAX_SIZE:  # if value > (65536 - 4096)
        value -= 65536
    return value / 256

  def __init__(self, data: bytes):
    assert len(data) >= 8, f"Vertex data must be at least 8 bytes, got {len(data)}"
    stream = BytesIO(data)

    # Read and scale coordinates
    self.x = self.read_coord(stream)
    self.y = self.read_coord(stream)
    self.z = self.read_coord(stream)
    
    # Skip 2 unknown bytes
    stream.read(2)

  def __repr__(self):
    return f"Vertex(x={self.x}, y={self.y}, z={self.z})"