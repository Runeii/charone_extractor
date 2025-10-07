from dataclasses import dataclass
from typing import List
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
        self.calculate_bone_positions()
        
    def construct_bones(self, formatted_model: FormattedModel) -> List[ConstructedBone]:
        formatted_bones = formatted_model.bones
        return list(map(lambda i, _: ConstructedBone(formatted_model, i), range(len(formatted_bones)), formatted_bones))

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

    def calculate_bone_positions(self) -> None:
      direction = Vector((0.0, 1.0, 0.0))

      for i, bone in enumerate(self.bones):
          if i == 0:
              bone.head = [0.0, 0.0, 0.0]
              bone.length = -0.5
          else:
              if bone.parent is not None:
                  bone.head = self.bones[bone.parent].tail
              
          scaled_length = bone.length / 256.0

          bone.tail = [
              bone.head[0] + direction.x * scaled_length,
              bone.head[1] + direction.y * scaled_length,
              bone.head[2] + direction.z * scaled_length
          ]
