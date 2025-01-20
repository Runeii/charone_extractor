from dataclasses import dataclass, field
from io import BytesIO
from ...utils.binary_reader import BinaryReader

@dataclass
class SkinObject:
  """A skin object in the MCH format (8 bytes total).
  
  Structure:
  - first_vertex_index (2 bytes): SHORT - index of first vertex (0-based)
  - vertex_count (2 bytes): SHORT - number of vertices
  - bone_id (2 bytes): SHORT - bone ID (1-based, converted to 0-based)
  - unknown (2 bytes): SHORT - unknown value (skipped)
  """
  data: bytes

  first_vertex_index: int = field(init=False)
  vertex_count: int = field(init=False)
  bone_id: int = field(init=False)

  def __post_init__(self):
    assert len(self.data) >= 8, f"Vertex data must be at least 8 bytes, got {len(self.data)}"
    stream = BytesIO(self.data)

    self.first_vertex_index = BinaryReader.read_uint16(stream)
    self.vertex_count = BinaryReader.read_uint16(stream)
    self.bone_id = BinaryReader.read_uint16(stream)

    stream.read(2)

  def __repr__(self):
    return (f"first_vertex_index:{self.first_vertex_index} "
            f"vertex_count:{self.vertex_count} bone_id:{self.bone_id} ")