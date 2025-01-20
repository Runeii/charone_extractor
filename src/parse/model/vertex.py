from dataclasses import dataclass, field
from io import BytesIO
from ...utils.binary_reader import BinaryReader

@dataclass
class Vertex:
  """A vertex in the MCH format.
  
  Structure:
  - x (2 bytes): SHORT - X position
  - y (2 bytes): SHORT - Y position
  - z (2 bytes): SHORT - Z position
  - unknown1 (2 bytes): SHORT - unknown value (skipped)
  """
  data: bytes

  x: float = field(init=False)
  y: float = field(init=False)
  z: float = field(init=False)

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    # Read and scale coordinates
    self.x = BinaryReader.read_uint16(stream)
    self.y = BinaryReader.read_uint16(stream)
    self.z = BinaryReader.read_uint16(stream)
    
    # Skip 2 unknown bytes
    stream.read(2)

  def __repr__(self):
    return f"Vertex(x={self.x}, y={self.y}, z={self.z})"