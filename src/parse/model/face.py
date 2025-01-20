from dataclasses import dataclass, field
from typing import List, Tuple
from io import BytesIO
from ...utils.binary_reader import BinaryReader

@dataclass
class Face:
  """A face in the MCH format (64 bytes total).
  
  Structure:
  - opcode (4 bytes): 0x07060125 = triangle, 0x0907012d = quad
  - unknown1 (4 bytes): unused
  - unknown_short (2 bytes): semitransparency when bit 0x04 is set
  - unknown2 (2 bytes): unused
  - vertices (8 bytes): four vertex IDs (2 bytes each)
  - edge_data (8 bytes): four edge values (2 bytes each)
  - vertex_colors (16 bytes): four color values (4 bytes each)
  - texture_coords (8 bytes): four uv pairs (2 bytes each)
  - padding1 (2 bytes): unused
  - texture_index (2 bytes): texture group/index
  - padding2 (8 bytes): unused
  """
  data: bytes

  opcode: int = field(init=False)
  vertices: List[int] = field(init=False)
  edge_data: List[int] = field(init=False)
  vertex_colors: List[int] = field(init=False)
  texture_coords: List[Tuple[int, int]] = field(init=False)
  texture_index: int = field(init=False)
  unknown_flags: int = field(init=False)


  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.opcode = BinaryReader.read_uint32(stream)
    
    __unknown = BinaryReader.read_uint32(stream)
    
    self.unknown_flags = BinaryReader.read_uint16(stream)
    
    __unknown2 = BinaryReader.read_uint16(stream)
    
    self.vertices = [
        BinaryReader.read_uint16(stream) for _ in range(4)
    ]
    
    self.edge_data = [
        BinaryReader.read_uint16(stream) for _ in range(4)
    ]
    
    self.vertex_colors = [
        BinaryReader.read_uint32(stream) for _ in range(4)
    ]
    
    self.texture_coords = [
        (BinaryReader.read_uint8(stream), BinaryReader.read_uint8(stream))
        for _ in range(4)
    ]
    
    __padding1 = BinaryReader.read_uint16(stream)
    
    self.texture_index = BinaryReader.read_uint16(stream)
    
    __padding2a = BinaryReader.read_uint32(stream)
    __padding2b = BinaryReader.read_uint32(stream)

  @property
  def has_semitransparency(self) -> bool:
      return bool(self.unknown_flags & 0x04)
      
  @property
  def is_quad(self) -> bool:
      return self.opcode == 0x2d010709
      
  @property 
  def is_triangle(self) -> bool:
      return self.opcode == 0x25010607
  