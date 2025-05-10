from dataclasses import dataclass, field
from ..parse.model.bone import Bone
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
  parent: int
  length: float
  name: str
  head: Tuple[float, float, float]
  tail: Tuple[float, float, float]

  bone: Bone

  parent_bone: int = field(init=False)
  bone_length: float = field(init=False)

  def __post_init__(self):
    self.parent_bone = self.bone.parent_bone - 1
    self.bone_length = self.bone.bone_length

  def sanitise_parent_bone(self):
    self.parent_bone = self.parent_bone - 1