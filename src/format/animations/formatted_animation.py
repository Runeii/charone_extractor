from dataclasses import dataclass
from typing import List
from .formatted_frame import FormattedFrame
from src.parse.model.animations.animation import Animation
from ...parse.model.animations.frame import Frame
from src.format.formatted_bone import FormattedBone

@dataclass(init=False)
class FormattedAnimation:
  name: str
  frame_count: int
  bone_count: int
  
  frames: List[FormattedFrame]
  bone_names: List[str]

  def __init__(self, original: Animation, bones: List[FormattedBone]):
    self.name = original.name
    self.frame_count = original.frame_count
    self.bone_count = original.bone_count

    self.frames = self.parse_frames(original.frames, bones)
    self.bone_names = [bone.name for bone in bones]

  def parse_frames(self, frames: List[Frame], bones: List[FormattedBone]) -> List[FormattedFrame]:
    parsed_frames: List[FormattedFrame] = []
    for frame_data in frames:
      frame = FormattedFrame(frame_data, bones)
      parsed_frames.append(frame)
    
    return parsed_frames