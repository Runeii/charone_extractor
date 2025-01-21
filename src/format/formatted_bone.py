from dataclasses import dataclass, field
from ..parse.model.bone import Bone

@dataclass
class FormattedBone:
  bone: Bone

  parent_bone: int = field(init=False)
  bone_length: float = field(init=False)

  def __post_init__(self):
    self.parent_bone = self.bone.parent_bone - 1
    self.bone_length = self.bone.bone_length

  def sanitise_parent_bone(self):
    self.parent_bone = self.parent_bone - 1