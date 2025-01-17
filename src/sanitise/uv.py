from dataclasses import dataclass, field
from typing import List, Tuple
import math

@dataclass
class UV:
  """Matches the UV format from first implementation with coordinate transformations"""
  coords: Tuple[int, int]
  texture_index: int

  u: int = field(init=False)
  v: int = field(init=False)

  def __post_init__(self):
    """Creates UV from raw coordinates and applies transformations"""
    u, v = self.coords

    # Get texture group offsets
    [tgroup_x, tgroup_y] = self.get_texture_offsets(self.texture_index)
    
    # Apply transformations:
    # 1. Invert V coordinate (128-v)
    v = 128 - v

    # 2. Apply texture group offsets
    u = u + (tgroup_x * 128)
    v = v + (tgroup_y * 128)

    self.u = int(u)
    self.v = int(v)
  
  @staticmethod
  def get_texture_offsets(index: int) -> list[int]:
      """Get texture offsets as [horizontal_multiplier, vertical_multiplier]
      
      Converts texture index into grid coordinates:
      - horizontal_multiplier = number of columns (floor division by 2)
      - vertical_multiplier = whether in top or bottom row (0 or 1)
      """
      return [math.floor(index/2), index % 2]

  def __repr__(self):
      return f"UV[{int(self.u)}, {int(self.v)}]"