from dataclasses import dataclass
from typing import List
import math
from mathutils import Euler, Vector

from src.format.formatted_bone import FormattedBone
from src.format.formatted_skin import FormattedSkin
from src.format.formatted_model import FormattedModel
from src.format.formatted_rest_pose import FormattedRestPoseBoneRotation

from .constructed_bone import ConstructedBone
@dataclass(init=False)
class ConstructedSkeleton:
    name: str
    bones: List[ConstructedBone]
    skins: List[FormattedSkin]  # Store skin data
    
    def __init__(self, formatted_model: FormattedModel):
        self.name = formatted_model.name
        self.formatted_skins = formatted_model.skin_objects;
        self.skins = formatted_model.skin_objects;

        self.bones = self.construct_bones(formatted_model.bones)
        self.calculate_bone_hierarchy()
        self.calculate_bone_positions(formatted_model)
        print(self.bones)
        
        
    def construct_bones(self, formatted_bones: List[FormattedBone]) -> List[ConstructedBone]:
        return list(map(lambda i, formatted_bone: ConstructedBone(formatted_bone, i, self.name), range(len(formatted_bones)), formatted_bones))

    def calculate_bone_hierarchy(self) -> None:
        for bone in self.bones:
            if bone.parent is not None:
                self.bones[bone.parent].child_count += 1
        
        for i in range(len(self.bones)):
          self.bones[i].chain_length = self.calculate_chain_length(i)

    def calculate_chain_length(self, bone_index: int) -> int:
        length = 1
        current = bone_index
        parent = self.bones[current].parent
        while parent is not None:
            length += 1
            current = parent
            parent = self.bones[current].parent
        return length

    # Use the rest pose to calculate the bone positions
    def calculate_bone_positions(self, formatted_model: FormattedModel) -> None:
      rest_pose_offset = [formatted_model.rest_pose.offset_x, formatted_model.rest_pose.offset_y, formatted_model.rest_pose.offset_z]

      for i, bone in enumerate(self.bones):
        rest_pose_rotation = self.get_rest_pose_rotation(bone.name, formatted_model.rest_pose.bone_rotations[i])

        direction = Vector((0.0, 0.0, 1.0))
        direction.rotate(rest_pose_rotation)
        
        if i == 0:
          bone.head = [0.0, 0.0, 0.0]
          bone.length = Vector((rest_pose_offset[0], rest_pose_offset[1], rest_pose_offset[2])).length
        else:
          parent_id = bone.parent

          # Warn if parent is invalid
          if parent_id is not None and (0 > parent_id or parent_id > len(self.bones)):
            raise Exception(f"Parent bone index {parent_id} is out of range for bone {bone.name}. Bones length: {len(self.bones)}")
              
          if parent_id is not None:
            parent = self.bones[parent_id]
            bone.head = parent.tail
        
        scaled_length = bone.length / 256.0
        bone.tail = [
            bone.head[0] + direction.x * scaled_length,
            bone.head[1] + direction.y * scaled_length,
            bone.head[2] + direction.z * scaled_length
        ]
        
        if i == 0:
          bone.roll = math.radians(90)
        elif i == 1 or \
          bone.name in ["neck", "head"] or \
          bone.name.startswith("hair") or \
          bone.name.startswith("cape") or \
          bone.name.startswith("collar"):
            bone.roll = math.radians(-90)
        else:
          bone.roll = math.radians(90)


    def get_rest_pose_rotation(self, bone_name: str, rotation: FormattedRestPoseBoneRotation) -> Euler:
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
