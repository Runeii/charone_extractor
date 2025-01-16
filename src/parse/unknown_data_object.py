from dataclasses import dataclass, field
from typing import List
from io import BytesIO
import struct

@dataclass
class UnknownDataObject:
  """A data structure for parsing unknown data related to skin objects, triangles, and quads.
  
  Structure:
  - start_skinobject_index (2 bytes): UINT16 - starting index of skin objects
  - skinobject_count (2 bytes): UINT16 - number of skin objects
  - unknown (12 bytes): 12 bytes of unknown data
  - start_triangle_index (2 bytes): UINT16 - starting index of triangles
  - triangle_count (2 bytes): UINT16 - number of triangles
  - start_quad_index (2 bytes): UINT16 - starting index of quads
  - quad_count (2 bytes): UINT16 - number of quads
  - unknown2 (8 bytes): 8 bytes of additional unknown data
  """
  data: bytes

  start_skinobject_index: int = field(init=None)
  skinobject_count: int = field(init=None)
  start_triangle_index: int = field(init=None)
  triangle_count: int = field(init=None)
  start_quad_index: int = field(init=None)
  quad_count: int = field(init=None)
  unknown: List[int] = field(init=None)
  unknown2: List[int] = field(init=None)

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.start_skinobject_index = self.read_uint16(stream)
    self.skinobject_count = self.read_uint16(stream)

    self.unknown = list(stream.read(12))

    self.start_triangle_index = self.read_uint16(stream)
    self.triangle_count = self.read_uint16(stream)

    self.start_quad_index = self.read_uint16(stream)
    self.quad_count = self.read_uint16(stream)

    self.unknown2 = list(stream.read(8))

  def __repr__(self):
    return (f"UnknownDataObject(skinobject_start={self.start_skinobject_index}, "
            f"skinobject_count={self.skinobject_count}, "
            f"triangle_start={self.start_triangle_index}, "
            f"triangle_count={self.triangle_count}, "
            f"quad_start={self.start_quad_index}, "
            f"quad_count={self.quad_count})")