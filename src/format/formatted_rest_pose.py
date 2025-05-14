from dataclasses import dataclass, field
from math import pi
from typing import List
from src.parse.model.rest_pose import RestPose, RestPoseBoneRotation

@dataclass(init=False)
class FormattedRestPoseBoneRotation:
  x: float = field(default=0)
  y: float = field(default=0)
  z: float = field(default=0)

  def __init__(self, bone_rotation: RestPoseBoneRotation):
    self.x = self.handle_negative_values(bone_rotation.x)
    self.y = self.handle_negative_values(bone_rotation.y)
    self.z = self.handle_negative_values(bone_rotation.z)

    self.x = self.convert_to_radians(self.x)
    self.y = self.convert_to_radians(self.y)
    self.z = self.convert_to_radians(self.z)
  
  def handle_negative_values(self, value: int):
    if value > 32767:
      return value - 65536
    return value

  def convert_to_radians(self, value: int):
    return pi * value / 2048

@dataclass
class FormattedRestPose:
  rest_pose: RestPose

  offset_x: int = field(default=0)
  offset_y: int = field(default=0)
  offset_z: int = field(default=0)

  bone_rotations: List[FormattedRestPoseBoneRotation] = field(default_factory=list)
  
  def __post_init__(self):
    self.offset_x = self.rest_pose.offset_x
    self.offset_y = self.rest_pose.offset_y
    self.offset_z = self.rest_pose.offset_z

    for bone_rotation in self.rest_pose.bone_rotations:
      self.bone_rotations.append(FormattedRestPoseBoneRotation(bone_rotation))
