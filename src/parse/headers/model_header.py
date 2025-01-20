from dataclasses import dataclass, field
from typing import List
from ...utils.binary_reader import BinaryReader
from io import BytesIO

@dataclass(init=False)
class ModelHeader:
  model_offset: int = field(init=False)
  data_size: int = field(init=False)
  model_id: int = field(init=False)

  is_main_field_model: bool = field(init=False)
  main_field_id: int = field(init=False)

  tim_offsets: List[int] = field(default_factory=list)
  model_data_offset: int = field(init=False)
  model_name: str = field(init=False)

  def __init__(self, stream: BytesIO):
    self.model_offset = BinaryReader.read_uint32(stream)
    self.data_size = BinaryReader.read_uint32(stream)
    self.model_id = BinaryReader.read_uint32(stream)

    ## Sometimes there is a duplicate data size field
    if self.data_size == self.model_id:
      self.model_id = BinaryReader.read_uint32(stream)
    
    self.is_main_field_model = self.model_id >> 24 == 0xd0

    self.tim_offsets = []

    if self.is_main_field_model:
      self.main_field_id = BinaryReader.read_uint32(stream)
    else:
      if (self.model_id & 0xFFFFFF) == 0:
        self.tim_offsets.append(0)
      
      while stream.tell() < 0x800:
        tim_offset = BinaryReader.read_uint32(stream)
        if tim_offset == 0xFFFFFFFF:
          break
        self.tim_offsets.append(tim_offset)
      
      self.model_data_offset = BinaryReader.read_uint32(stream)
    
    self.model_name = BinaryReader.read_string(stream)

    _spacer = BinaryReader.read_uint32(stream)
