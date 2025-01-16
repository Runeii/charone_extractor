from dataclasses import dataclass
from io import BytesIO
import struct

@dataclass
class SkinObject:
  """A skin object in the MCH format (8 bytes total).
  
  Structure:
  - first_vertex_index (2 bytes): SHORT - index of first vertex (0-based)
  - vertex_count (2 bytes): SHORT - number of vertices
  - bone_id (2 bytes): SHORT - bone ID (1-based, converted to 0-based)
  - unknown (2 bytes): SHORT - unknown value (skipped)
  """
  first_vertex_index: int
  vertex_count: int
  bone_id: int
  name: str = 'none'

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  def __init__(self, data: bytes):
    assert len(data) >= 8, f"SkinObject must be at least 8 bytes, got {len(data)}"
    stream = BytesIO(data)

    self.first_vertex_index = self.read_uint16(stream)
    self.vertex_count = self.read_uint16(stream)
    self.bone_id = self.read_uint16(stream)

    stream.read(2)

  def __repr__(self):
    return (f"vFirst:{self.first_vertex_index} "
            f"vCount:{self.vertex_count} bone:{self.bone_id} ")