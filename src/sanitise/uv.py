from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class UV:
  """Matches the UV format from first implementation with coordinate transformations"""
  u: int
  v: int
  texture_group: List[int]

  def get_texture_offsets(index: int) -> list[int]:
      """Get texture offsets as [horizontal_multiplier, vertical_multiplier]
      
      Converts texture index into grid coordinates:
      - horizontal_multiplier = number of columns (floor division by 2)
      - vertical_multiplier = whether in top or bottom row (0 or 1)
      """
      return [math.floor(index/2), index % 2]

  @classmethod
  def __init__(self, coords: Tuple[int, int], texture_index: int):
    """Creates UV from raw coordinates and applies transformations"""
    u, v = coords

    # Get texture group offsets
    [tgroup_x, tgroup_y] = self.get_texture_offsets(texture_index)
    
    # Apply transformations:
    # 1. Invert V coordinate (128-v)
    v = 128 - v

    # 2. Apply texture group offsets
    u = u + (tgroup_x * 128)
    v = v + (tgroup_y * 128)

    self.u = u
    self.v = v