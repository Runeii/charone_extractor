from dataclasses import dataclass, field
from typing import List
from .bone_pose import BonePose

## Extends BonePose to include a location property
@dataclass(init=False)
class RootBonePose(BonePose):
  location: List[int]

  def __init__(self, pose_data: List[bytes], offset: List[int], bone_length: float):
    # Call the parent class constructor
    super().__init__(pose_data)
    
    self.location = [
        offset[0],
        offset[2] - bone_length/256,
        offset[1]
    ]