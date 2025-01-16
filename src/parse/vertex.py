from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO
import struct

MAX_SIZE = 4096
@dataclass
class Vertex:
  """A vertex in the MCH format.
  
  Structure:
  - x (2 bytes): SHORT - X position
  - y (2 bytes): SHORT - Y position
  - z (2 bytes): SHORT - Z position
  - unknown1 (2 bytes): SHORT - unknown value (skipped)
  """
  x: float
  y: float
  z: float

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
      return struct.unpack("<H", stream.read(2))[0]

  def __init__(self, data: bytes):
    assert len(data) >= 8, f"Vertex data must be at least 8 bytes, got {len(data)}"
    stream = BytesIO(data)

    # Read and scale coordinates
    self.x = self.read_uint16(stream)
    self.y = self.read_uint16(stream)
    self.z = self.read_uint16(stream)
    
    # Skip 2 unknown bytes
    stream.read(2)

  def __repr__(self):
    return f"Vertex(x={self.x}, y={self.y}, z={self.z})"