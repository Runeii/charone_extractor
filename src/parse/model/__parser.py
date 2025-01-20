from dataclasses import dataclass, field
from .tim import TIM
from .model_data import ModelData
from ..headers.model_header import ModelHeader
from ..mch.mch_header import MCHHeader
from typing import List

@dataclass
class ModelParser:
  header: ModelHeader
  model_data: ModelData = field(init=False)
  textures: List[TIM] = field(init=False)

  def __init__(self, header: ModelHeader, data: bytes):
    self.header = header

    if header.is_main_field_model:
      self.parse_main_character_model(name=header.model_name, char_one_data=data[header.model_offset + 4:])
    else:
      self.parse_non_main_character_model(data)

  def parse_main_character_model(self, name: str, char_one_data: bytes):
    sanitised_name = name.replace("x", "")
    with open(f"./INPUT/models/{sanitised_name}.mch", "rb") as f:
      data = f.read()

    mch_header = MCHHeader(data[:256])

    self.model_data = ModelData(
      data=data,
      name=self.header.model_name,
      offset=mch_header.model_data_offset,
      char_one_data=char_one_data, # wiki: should note animation data location
    )

    self.textures = self.parse_textures(data, mch_header.tim_offsets)

  def parse_non_main_character_model(self, data: bytes):
    self.model_data = ModelData(
      data=data,
      name=self.header.model_name,
      offset=self.header.model_offset + self.header.model_data_offset + 4,
    )
    
    # Note: need to +4 for PC files
    tim_offsets = list(
      map(
        lambda tim_offset: self.header.model_offset + tim_offset + 4, self.header.tim_offsets
        )
    );
    
    self.textures = self.parse_textures(data, tim_offsets)

  def parse_textures(self, data: bytes, offsets: List[int]):
    textures: List[TIM] = []

    for offset in offsets:
      tim = TIM(
        name=self.header.model_name,
        data=data[offset:]
      )

      textures.append(tim)
    
    return textures
