from dataclasses import dataclass
from typing import List
from ...parse.model.animations.pose import Pose
from .bone_pose import BonePose

## Extends BonePose to include a location property
@dataclass(init=False)
class RootBonePose(BonePose):
  location: List[float]

  def __init__(self, pose: Pose, offset: List[float], bone_length: float):
    # Call the parent class constructor
    super().__init__(original=pose)
    
    self.location = [
        offset[0],
        offset[2] - bone_length/256,
        offset[1]
    ]