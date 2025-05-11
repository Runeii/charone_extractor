from dataclasses import dataclass, field
from src.parse.model.bone import Bone
from typing import Tuple

@dataclass
class FormattedBone:
  """Bone data from MCH format.
  
  Attributes:
      parent: Index of parent bone (-1 for root)
      length: Length of the bone
      name: Name of the bone
      head: Head position (x, y, z)
      tail: Tail position (x, y, z)
  """

  bone: Bone

  parent_bone: int = field(init=False)
  bone_length: float = field(init=False)

  parent_bone_offset: int = field(init=False) # wiki needs update: this is parent bone offset! (so multiple of 64)

  def __post_init__(self):
    self.parent_bone = self.bone.parent_bone - 1
    self.bone_length = self.bone.bone_length

    self.parent_bone_offset = self.bone.parent_bone_offset  # currently unused