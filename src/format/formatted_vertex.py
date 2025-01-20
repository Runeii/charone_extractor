from dataclasses import dataclass, field
from ..parse.model.vertex import Vertex

MAX_SIZE = 4096

@dataclass(init=False)
class FormattedVertex:
  """From MCH2Blend, scale and detect negatives
  
  Structure:
  - x (2 bytes): SHORT - X position scaled by 1/256
  - y (2 bytes): SHORT - Y position scaled by 1/256
  - z (2 bytes): SHORT - Z position scaled by 1/256
  Note: Coordinates use 16-bit values with MAX_SIZE = 4096 for negative detection
  """

  x: float = field(init=False)
  y: float = field(init=False)
  z: float = field(init=False)

  def __init__(self, vertex: Vertex):
    self.x = self.sanitise_coord(vertex.x)
    self.y = self.sanitise_coord(vertex.y)
    self.z = self.sanitise_coord(vertex.z)

  @staticmethod
  def sanitise_coord(value: float) -> float:
    if value > 65536 - MAX_SIZE:
        value -= 65536
    return value / 256