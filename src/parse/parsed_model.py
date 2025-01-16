from dataclasses import dataclass
from .tim import TIM
from .model_data import ModelData

@dataclass
class ParsedModel:
  id: int
  name: str
  tim_offset: int
  model_offset: int
  data_offset: int
  data: bytes
  tim: TIM = None

  def __init__(self, id: int, name: str, model_offset: int, tim_offsets: int, data_offset: int, data: bytes):
    self.id = id
    self.name = name.replace('HXh', '')
    self.tim_offset = tim_offsets[0] if tim_offsets else False
    self.model_offset = model_offset
    self.data_offset = data_offset
    self.data = data

    self.model_data = ModelData(self.name, self.data, self.model_offset + self.data_offset + 4)

    # Note: need to +4 for PC files
    self.tim = TIM(self.name, self.data[self.model_offset + self.tim_offset + 4:]) if self.tim_offset is not None else None

  def __str__(self):
    return (
        f"Model {self.name}\n"
        f"  ID: 0x{self.id:08X}\n"
        f"  TIM: {self.tim}\n"
        f"  Model offset: {self.model_offset}\n"
        f"  TIM offset: {self.tim_offset}\n"
        f"  Data offset: {self.data_offset}\n"
        f"  Data size: {len(self.data) - self.model_offset} bytes"
    )