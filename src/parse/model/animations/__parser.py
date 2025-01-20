from dataclasses import dataclass, field
from io import BytesIO
from typing import List
from .animation import Animation
from ....utils.binary_reader import BinaryReader

@dataclass
class AnimationsParser:
  model_name: str
  data: bytes

  number_of_animations: int = field(init=False)
  animations: List[Animation] = field(init=False)

  def __post_init__(self):
    stream = BytesIO(self.data)
    self.number_of_animations = BinaryReader.read_uint16(stream)
    self.animations = self.parse_animations(self.number_of_animations, 2)

  def parse_animations(self, number_of_animations: int, offset_of_animations: int) -> List[Animation]:
    stream = BytesIO(self.data[offset_of_animations:])
    animations: List[Animation] = []

    for _ in range(number_of_animations):
      frame_count = BinaryReader.read_uint16(stream)
      bone_count = BinaryReader.read_uint16(stream)

      animation_size = Animation.calculate_size(frame_count, bone_count)
      animation_data = stream.read(animation_size)

      animation = Animation("{model_name}_action_{i}", frame_count, bone_count, animation_data)
      animations.append(animation)
    
    return animations