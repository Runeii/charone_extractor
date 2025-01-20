from dataclasses import dataclass, field
from io import BytesIO
from typing import List
from .frame import Frame

## wiki is OOD for all of this
@dataclass
class Animation:
  name: str
  frame_count: int
  bone_count: int
  data: bytes
  
  frames: List[Frame] = field(default_factory=list)

  def __post_init__(self):
    self.frames = self.parse_frames(self.frame_count)
  
  def parse_frames(self, number_of_frames: int):
    stream = BytesIO(self.data)
    frames = []
    for i in range(number_of_frames):
      frame_data = stream.read(Frame.calculate_size(self.bone_count))
      frame = Frame(self.bone_count, frame_data)
      frames.append(frame)
    
    return frames
  
  @staticmethod
  def calculate_size(frame_count: int, bone_count: int):
    return frame_count * Frame.calculate_size(bone_count)