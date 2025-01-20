from dataclasses import dataclass, field
from typing import List, Tuple
from io import BytesIO
from ...utils.binary_reader import BinaryReader

@dataclass(init=False)
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

  unknown1: int = field(init=False)
  total_textures: int = field(init=False)
  unknown2: int = field(init=False)
  u_size: int = field(init=False)
  v_size: int = field(init=False)
  replacement_coords_count: int = field(init=False)
  original_area_coords: Tuple[int, int] = field(init=False)
  replacement_coords: List[Tuple[int, int]] = field(init=False)

  @staticmethod
  def read_uv_pair(stream: BytesIO) -> Tuple[int, int]:
    """Read a UV coordinate pair (two unsigned bytes)."""
    return (
        BinaryReader.read_uint8(stream), 
        BinaryReader.read_uint8(stream)
    )

  def __init__(self, stream: BytesIO):
    # Read initial bytes
    self.unknown1 = BinaryReader.read_uint8(stream)
    self.total_textures = BinaryReader.read_uint8(stream)
    self.unknown2 = BinaryReader.read_uint8(stream)
    self.u_size = BinaryReader.read_uint8(stream)
    self.v_size = BinaryReader.read_uint8(stream)
    
    # Read replacement section count
    self.replacement_coords_count = BinaryReader.read_uint8(stream)

    # Read original area coordinates
    self.original_area_coords = self.read_uv_pair(stream)
    # Skip 2 unknown bytes
    stream.read(2)

    # Read replacement coordinates
    self.replacement_coords = [
        self.read_uv_pair(stream) 
        for _ in range(self.replacement_coords_count)
    ]

  def __repr__(self):
      return (f"TextureAnimation(total_textures={self.total_textures}, "
              f"u_size={self.u_size}, v_size={self.v_size}, "
              f"replacement_sections={self.replacement_coords_count})")