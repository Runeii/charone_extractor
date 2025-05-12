from dataclasses import dataclass, field
from typing import List, Tuple
from src.parse.model.face import Face

@dataclass(init=False)
class FormattedFace:
  """Reorder vertices to match the order in the MCH2Blend format"""

  is_triangle: bool = field(init=False)

  v1: int = field(init=False)
  v2: int = field(init=False)
  v3: int = field(init=False)
  v4: int | None = field(init=False)
  texture_coords: List[Tuple[int, int]] = field(init=False)
  texture_index: int = field(init=False)
  vt1: int = field(init=False)  # UV index for v1
  vt2: int = field(init=False)  # UV index for v2
  vt3: int = field(init=False)  # UV index for v3
  vt4: int | None = field(init=False)  # UV index for v4
  
  def __init__(self, face: Face):
    self.is_triangle = face.opcode == 620824071

    # Order vertices to match MCH2Blend format
    self.v1 = face.vertices[1]  # Second vertex
    self.v2 = face.vertices[0]  # First vertex
    self.v3 = face.vertices[2]  # Third vertex
    self.v4 = face.vertices[3] if len(face.vertices) == 4 else None  # Fourth vertex (if quad)
    
    # Order texture coordinates to match vertex order
    if len(face.texture_coords) >= 4:
      self.texture_coords = [
        face.texture_coords[1],  # v1
        face.texture_coords[0],  # v2
        face.texture_coords[2],  # v3
        face.texture_coords[3]   # v4
      ]
    else:
      self.texture_coords = face.texture_coords
      
    self.texture_index = face.texture_index
    
    # Initialize UV indices (will be set during UV construction)
    self.vt1 = 0
    self.vt2 = 0
    self.vt3 = 0
    self.vt4 = None

    def __repr__(self) -> str:
        return f"Face: v1={self.v1} v2={self.v2} v3={self.v3} v4={self.v4}"
