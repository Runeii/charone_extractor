from dataclasses import dataclass
from ..format.formatted_model import FormattedBone
from src.format.bone_names import get_bone_name
from typing import Optional, List

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

  def __init__(self, formatted_bone: FormattedBone, bone_index: int, model_name: str):
    self.formatted_bone = formatted_bone

    self.name = get_bone_name(bone_index, model_name)
    self.parent = formatted_bone.parent_bone if formatted_bone.parent_bone >= 0 else None
    self.length = formatted_bone.bone_length

    self.child_count = 0
    self.chain_length = 1
    self.head = [0.0, 0.0, 0.0]
    self.tail = [0.0, 0.0, 0.0]
    self.roll = 0.0