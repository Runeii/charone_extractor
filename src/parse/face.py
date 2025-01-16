from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO
import struct

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
  opcode: int
  vertices: List[int]  # 4 vertex IDs
  edge_data: List[int]  # 4 edge values
  vertex_colors: List[int]  # 4 color values
  texture_coords: List[Tuple[int, int]]  # 4 uv pairs
  texture_index: int
  unknown_flags: int  # Contains semitransparency bit

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
      return struct.unpack("<I", stream.read(4))[0]
      
  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
      return struct.unpack("<H", stream.read(2))[0]
      
  @staticmethod
  def read_uint8(stream: BytesIO) -> int:
      return struct.unpack("<B", stream.read(1))[0]

  def __init__(self, data: bytes):
    assert len(data) == 64, f"Face must be 64 bytes, got {len(data)}"
    stream = BytesIO(data)

    self.opcode = self.read_uint32(stream)
    print(self.opcode)
    
    __unknown = self.read_uint32(stream)
    
    self.unknown_flags = self.read_uint16(stream)
    
    __unknown2 = self.read_uint16(stream)
    
    self.vertices = [
        self.read_uint16(stream) for _ in range(4)
    ]
    
    self.edge_data = [
        self.read_uint16(stream) for _ in range(4)
    ]
    
    self.vertex_colors = [
        self.read_uint32(stream) for _ in range(4)
    ]
    
    self.texture_coords = [
        (self.read_uint8(stream), self.read_uint8(stream))
        for _ in range(4)
    ]
    
    __padding1 = self.read_uint16(stream)
    
    self.texture_index = self.read_uint16(stream)
    
    __padding2a = self.read_uint32(stream)
    __padding2b = self.read_uint32(stream)

  @property
  def has_semitransparency(self) -> bool:
      return bool(self.unknown_flags & 0x04)
      
  @property
  def is_quad(self) -> bool:
      return self.opcode == 0x0907012d
      
  @property 
  def is_triangle(self) -> bool:
      return self.opcode == 0x07060125