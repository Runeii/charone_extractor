from dataclasses import dataclass
from typing import List
from ...parse.model.animations.frame import Frame
from ...parse.model.animations.pose import Pose

from .bone_pose import BonePose
from .root_bone_pose import RootBonePose
from ..formatted_bone import FormattedBone

@dataclass(init=False) 
class FormattedFrame:
  poses: List[BonePose]

  def __init__(self, original: Frame, bones: List[FormattedBone]):
    scaled_offset = self.scale_offset(original.coordinate_offset)

    self.poses = self.construct_bone_poses(original.poses, scaled_offset, bones)
  
  @staticmethod
  def scale_offset(offset: List[int]):
    return [int(x) / 256 for x in offset]

  def construct_bone_poses(self, poses: List[Pose], root_offset: List[float], bones: List[FormattedBone]):
    parsed_poses: List[BonePose] = []
    for i, pose in enumerate(poses):
      if i == 0:
        parsed_poses.append(RootBonePose(
          pose=pose,
          offset=root_offset,
          bone_length=bones[0].bone_length
        ))
        continue
      parsed_poses.append(BonePose(original=pose))
    
    return parsed_poses