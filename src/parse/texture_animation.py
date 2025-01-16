from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO
import struct

@dataclass
class TextureAnimation:
  """A data structure for parsing texture animation information.
  
  Structure:
  - unknown1 (1 byte): first unknown byte
  - total_textures (1 byte): total number of textures
  - unknown2 (1 byte): second unknown byte
  - u_size (1 byte): u-dimension size
  - v_size (1 byte): v-dimension size
  - replacement_section_count (1 byte): number of replacement sections
  - original_area_coords (Tuple[int, int]): original UV coordinates
  - replacement_coords (List[Tuple[int, int]]): list of replacement UV coordinates
  """
  unknown1: int
  total_textures: int
  unknown2: int
  u_size: int
  v_size: int
  replacement_section_count: int
  original_area_coords: Tuple[int, int]
  replacement_coords: List[Tuple[int, int]]

  @staticmethod
  def read_uint8(stream: BytesIO) -> int:
    return struct.unpack("<B", stream.read(1))[0]

  @staticmethod
  def read_uv_pair(stream: BytesIO) -> Tuple[int, int]:
    """Read a UV coordinate pair (two unsigned bytes)."""
    return (
        TextureAnimation.read_uint8(stream), 
        TextureAnimation.read_uint8(stream)
    )

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    # Read initial bytes
    self.unknown1 = self.read_uint8(stream)
    self.total_textures = self.read_uint8(stream)
    self.unknown2 = self.read_uint8(stream)
    self.u_size = self.read_uint8(stream)
    self.v_size = self.read_uint8(stream)
    
    # Read replacement section count
    self.replacement_section_count = self.read_uint8(stream)

    # Read original area coordinates
    self.original_area_coords = self.read_uv_pair(stream)

    # Skip 2 unknown bytes
    stream.read(2)

    # Read replacement coordinates
    self.replacement_coords = [
        self.read_uv_pair(stream) 
        for _ in range(self.replacement_section_count)
    ]

  def __repr__(self):
      return (f"TextureAnimation(total_textures={self.total_textures}, "
              f"u_size={self.u_size}, v_size={self.v_size}, "
              f"replacement_sections={self.replacement_section_count})")