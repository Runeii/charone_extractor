from dataclasses import dataclass, field
from ..parse.model.face import Face

@dataclass
class SanitisedFace:
  """Converts from the detailed Face format to simplified format"""
  face: Face

  v1: int = field(init=False)
  v2: int = field(init=False)
  v3: int = field(init=False)
  v4: int = field(init=False)
  
  def __post_init__(self):
    # Reorder vertices to match the order in the MCH2Blend format
    self.v2 = self.face.vertices[0]
    self.v1 = self.face.vertices[1]
    self.v3 = self.face.vertices[2]
    self.v4 = self.face.vertices[3]
