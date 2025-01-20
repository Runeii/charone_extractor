from dataclasses import dataclass
from .tim import TIM
from .model import Model
from ..headers.model_header import ModelHeader

@dataclass
class ModelParser:
  header: ModelHeader
  model: Model
  tim: TIM

  def __init__(self, header: ModelHeader, data: bytes):

    model = Model(
      header=header,
      data=data,
      offset=header.model_offset + header.model_data_offset + 4,
    )

    tim_offset = self.tim_offsets[0] if self.tim_offsets else None
    
    # Note: need to +4 for PC files
    tim = TIM(self.name, self.data[self.model_offset + tim_offset + 4:]) if tim_offset is not None else None
  
    self.model = model
    self.tim = tim