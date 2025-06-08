from dataclasses import dataclass
from typing import List
from src.parse.model.animations.pose import Pose
from .bone_pose import BonePose

## Extends BonePose to include a location property
@dataclass(init=False)
class RootBonePose(BonePose):
  location: List[float]

  def __init__(self, pose: Pose, offset: List[int]):
    # Call the parent class constructor
    super().__init__(original=pose)
    
    self.location = [
        offset[0] / 256,
        offset[1] / 256,
        offset[2] / 256,
    ]