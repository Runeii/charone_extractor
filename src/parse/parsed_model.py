from dataclasses import dataclass, field
from .model.tim import TIM
from .model.model_data import ModelData

@dataclass
class ParsedModel:
  id: int
  name: str
  tim_offsets: list[int]
  model_offset: int
  data_offset: int
  data: bytes

  tim_offset: int = field(init=None)
  model_data: ModelData = field(init=None)
  tim: TIM = field(init=None)

  def __post_init__(self):
    self.name = self.name.replace('HXh', '')

    self.model_data = ModelData(self.name, self.data, self.model_offset + self.data_offset + 4)
    # Note: need to +4 for PC files
    tim_offset = self.tim_offsets[0] if self.tim_offsets else None
    self.tim = TIM(self.name, self.data[self.model_offset + tim_offset + 4:]) if tim_offset is not None else None

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