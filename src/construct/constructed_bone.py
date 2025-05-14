from dataclasses import dataclass
from ..format.formatted_model import FormattedBone, FormattedModel
from ..format.formatted_rest_pose import FormattedRestPoseBoneRotation
from src.format.bone_names import get_bone_name
from typing import List
from mathutils import Euler
import math

@dataclass(init=False)
class ConstructedBone:
  formatted_bone: FormattedBone

  name: str
  parent: int | None
  length: float

  child_count: int
  chain_length: int
  head: List[float]
  tail: List[float]
  roll: float

  rest_pose_rotation: Euler

  def __init__(self, formatted_model: FormattedModel, bone_index: int, model_name: str):
    formatted_bone = formatted_model.bones[bone_index]

    self.formatted_bone = formatted_bone

    self.name = get_bone_name(bone_index, model_name)
    self.parent = formatted_bone.parent_bone if formatted_bone.parent_bone >= 0 else None
    self.length = formatted_bone.bone_length

    self.child_count = 0
    self.chain_length = 1
    self.head = [0.0, 0.0, 0.0]
    self.tail = [0.0, 0.0, 0.0]
    self.roll = 0.0

    self.rest_pose_rotation = self.get_rest_pose_rotation(formatted_model.rest_pose.bone_rotations[bone_index])


  def get_rest_pose_rotation(self, rotation: FormattedRestPoseBoneRotation) -> Euler:
      bone_name = self.name

      eul = Euler((rotation.x, rotation.y, rotation.z), 'YXZ')

      if(bone_name=="upperbody"):
          eul.rotate_axis('Y',math.radians(-85))
      if(bone_name=="lowerbody"):
          if rotation.x > 0:
              eul.rotate_axis('Y',math.radians(-90))
          else:
              eul.rotate_axis('Y',math.radians(90))
      if bone_name == "neck":
          eul.rotate_axis('Y', math.radians(180))
      elif bone_name == "head":
          eul.rotate_axis('Y', math.radians(170))
      elif bone_name == "hair0":
          eul.rotate_axis('Y', math.radians(150))
      elif bone_name == "hair1" or bone_name == "hair2":
          eul.y = 0
      elif bone_name == "hair3":
          eul.rotate_axis('Y', math.radians(-45))
      elif bone_name == "collar0" or bone_name == "collar2":
          eul.x = 0
          eul.rotate_axis('Z', math.radians(-30))
          eul.rotate_axis('Y', math.radians(-90))
      elif bone_name == "collar1":
          eul.x = 0
          eul.rotate_axis('X', math.radians(90))
          eul.rotate_axis('Y', math.radians(30))
      elif bone_name == "collar3":
          eul.x = 0
          eul.rotate_axis('X', math.radians(-90))
          eul.rotate_axis('Y', math.radians(30))
      elif bone_name == "cape0" or bone_name == "cape1":
          eul.x = 0
          eul.y = 0
          eul.z = 0
          eul.rotate_axis('Y', math.radians(-20))
      elif bone_name == "cape3":
          eul.x = 0
      elif bone_name == "cape4":
          eul.x = 0
          eul.y = 0
          eul.z = 0
      elif bone_name == "dress1" or bone_name == "dress4":
          eul.rotate_axis('Y',math.radians(90))
          eul.rotate_axis('Z',math.radians(90))
      elif bone_name == "dress0" or bone_name == "dress3":
          eul.z = 0
          eul.y = 0
          eul.x = 0
      elif bone_name == "dress2" or bone_name == "dress5":
          eul.z = 0
      elif bone_name == "belt0":
          eul.rotate_axis('Y', math.radians(100))
          eul.rotate_axis('X', math.radians(-10))
      elif bone_name == "belt1":
          eul.rotate_axis('Y', math.radians(100))
          eul.rotate_axis('X', math.radians(10))
      elif bone_name == "belt2":
          eul.rotate_axis('Z', math.radians(30))
          eul.rotate_axis('Y', math.radians(120))
      elif bone_name == "belt4":
          eul.rotate_axis('Z', math.radians(-30))
          eul.rotate_axis('Y', math.radians(120))
      elif bone_name == "belt3":
          eul.rotate_axis('Y', math.radians(90))
          eul.rotate_axis('X', math.radians(-45))
      elif bone_name == "belt5":
          eul.rotate_axis('Y', math.radians(90))
          eul.rotate_axis('Z', math.radians(45))
      elif bone_name == "breast_R":
          eul.rotate_axis('Y', math.radians(45))
          eul.rotate_axis('X', math.radians(-10))
      elif bone_name == "breast_L":
          eul.rotate_axis('Y', math.radians(45))
          eul.rotate_axis('X', math.radians(10))
          eul.rotate_axis('Z', math.radians(180))
      elif bone_name == "shoulder_R":
          eul.rotate_axis('Y', math.radians(45))
          eul.rotate_axis('Z', math.radians(70))
          eul.rotate_axis('X', math.radians(15))
      elif bone_name == "shoulder_L":
          eul.rotate_axis('Y', math.radians(45))
          eul.rotate_axis('Z', math.radians(-70))
          eul.rotate_axis('X', math.radians(-15))
      elif bone_name == "hip_R" or bone_name == "hip_L":
          eul.y = 0
          eul.z = 0
          eul.rotate_axis('Y', math.radians(-20))
      elif bone_name == "thigh_R" or bone_name == "thigh_L":
          eul.x = 0
          eul.y = 0
          eul.z = 0
          
      return eul
