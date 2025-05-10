from dataclasses import dataclass, field
from typing import List, Tuple
from ..parse.model.face import Face

@dataclass(init=False)
class FormattedFace:
  """Reorder vertices to match the order in the MCH2Blend format"""

  v1: int = field(init=False)
  v2: int = field(init=False)
  v3: int = field(init=False)
  v4: int | None = field(init=False)
  texture_coords: List[Tuple[int, int]] = field(init=False)
  texture_index: int = field(init=False)
  
  def __init__(self, face: Face):
    self.v2 = face.vertices[0]
    self.v1 = face.vertices[1]
    self.v3 = face.vertices[2]
    self.v4 = face.vertices[3] if len(face.vertices) == 4 else None
    self.texture_coords = face.texture_coords
    self.texture_index = face.texture_index

    def __repr__(self) -> str:
        return f"Face: v1={self.v1} v2={self.v2} v3={self.v3} v4={self.v4}"
