from dataclasses import dataclass, field
from typing import List
from .frame import Frame
from ...parse.animation.animation import Animation as ParsedAnimation
from ..sanitised_bone import SanitisedBone

@dataclass(init=False)
class Animation:
  name: str
  frame_count: int
  bone_count: int
  
  frames: List[Frame]

  def __init__(self, original: ParsedAnimation, bones: List[SanitisedBone]):
    self.name = original.name
    self.frame_count = original.frame_count
    self.bone_count = original.bone_count

    self.frames = self.parse_frames(original.frames, bones)

  def parse_frames(self, frames: List[bytes], bones: List[SanitisedBone]):
    parsed_frames = []
    for frame_data in frames:
      frame = Frame(frame_data, bones)
      parsed_frames.append(frame)
    
    return parsed_frames