from dataclasses import dataclass
from typing import List
import math
from mathutils import Vector
from src.format.formatted_skin import FormattedSkin
from src.format.formatted_model import FormattedModel

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

        self.bones = self.construct_bones(formatted_model)
        self.calculate_bone_hierarchy()
        self.calculate_bone_positions(formatted_model)
        
    def construct_bones(self, formatted_model: FormattedModel) -> List[ConstructedBone]:
        formatted_bones = formatted_model.bones
        return list(map(lambda i, _: ConstructedBone(formatted_model, i, self.name), range(len(formatted_bones)), formatted_bones))

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
        direction = Vector((0.0, 0.0, 1.0))
        direction.rotate(bone.rest_pose_rotation)
        
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

