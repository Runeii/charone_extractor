from dataclasses import dataclass, field
from ..parse.model.vertex import Vertex

MAX_SIZE = 4096

@dataclass
class SanitisedVertex:
  """From MCH2Blend, scale and detect negatives
  
  Structure:
  - x (2 bytes): SHORT - X position scaled by 1/256
  - y (2 bytes): SHORT - Y position scaled by 1/256
  - z (2 bytes): SHORT - Z position scaled by 1/256
  Note: Coordinates use 16-bit values with MAX_SIZE = 4096 for negative detection
  """
  vertex: Vertex

  x: float = field(init=None)
  y: float = field(init=None)
  z: float = field(init=None)

  def __post_init__(self):
    self.x = self.sanitise_coord(self.vertex.x)
    self.y = self.sanitise_coord(self.vertex.y)
    self.z = self.sanitise_coord(self.vertex.z)

  @staticmethod
  def sanitise_coord(value: int) -> float:
    if value > 65536 - MAX_SIZE:
        value -= 65536
    return value / 256