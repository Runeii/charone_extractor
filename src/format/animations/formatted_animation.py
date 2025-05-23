from dataclasses import dataclass
from typing import List
from .formatted_frame import FormattedFrame
from src.parse.model.animations.animation import Animation
from ...parse.model.animations.frame import Frame

@dataclass(init=False)
class FormattedAnimation:
  name: str
  frame_count: int
  bone_count: int
  
  frames: List[FormattedFrame]

  def __init__(self, original: Animation):
    self.name = original.name
    self.frame_count = original.frame_count
    self.bone_count = original.bone_count

    self.frames = self.parse_frames(original.frames)

  def parse_frames(self, frames: List[Frame]) -> List[FormattedFrame]:
    parsed_frames: List[FormattedFrame] = []
    for frame_data in frames:
      frame = FormattedFrame(frame_data)
      parsed_frames.append(frame)
    
    
    return parsed_frames