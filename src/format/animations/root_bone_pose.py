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
      self.scale_offset(
        self.handle_negative_bone_length(offset[1])
      ),
      -self.scale_offset(
        self.handle_negative_bone_length(offset[0])
      ),
      self.scale_offset(
        self.handle_negative_bone_length(offset[2])
      ),
    ]
  
  def handle_negative_bone_length(self, bone_length: int):
    if bone_length > 32768:
        return bone_length - 65536
    return bone_length
  
  def scale_offset(self, offset: int):
    return offset / 256