from dataclasses import dataclass
from ..parse.face import Face
import math

@dataclass
class SanitisedFace:
  """Converts from the detailed Face format to simplified format"""
  opcode: int
  v1: int
  v2: int
  v3: int
  v4: int
  
  @classmethod
  def __init__(self, face: Face):
    self.opcode = face.opcode

    # Reorder vertices to match the order in the MCH2Blend format
    self.v2 = face.vertices[0]
    self.v1 = face.vertices[1]
    self.v3 = face.vertices[2]
    self.v4 = face.vertices[3]

  @property
  def is_quad(self) -> bool:
      return self.opcode == 0x0907012d
      
  @property 
  def is_triangle(self) -> bool:
      return self.opcode == 0x07060125