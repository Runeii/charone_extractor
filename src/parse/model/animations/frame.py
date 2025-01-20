import struct
from dataclasses import dataclass, field
from io import BytesIO
from typing import List
from ....utils.binary_reader import BinaryReader
from .pose import Pose

@dataclass
class Frame:
  bone_count: int
  data: bytes

  coordinate_offset: List[int] = field(init=False)
  poses: List[Pose] = field(init=False)
  
  def __post_init__(self):
    stream = BytesIO(self.data)
    
    self.coordinate_offset = [
      BinaryReader.read_int16(stream),
      BinaryReader.read_int16(stream),
      BinaryReader.read_int16(stream)
    ]

    self.poses = self.parse_poses(self.bone_count, 6)
  
  def parse_poses(self, number_of_poses: int, offset_of_poses: int):
    stream = BytesIO(self.data[offset_of_poses:])
    poses = []
    for i in range(number_of_poses):
      pose_data = stream.read(Pose.calculate_size())
      pose = Pose(pose_data)
      poses.append(pose)
    
    return poses
  
  @staticmethod
  def calculate_size(bone_count: int):
    return 6 + (bone_count * Pose.calculate_size())