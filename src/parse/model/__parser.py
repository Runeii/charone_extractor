from dataclasses import dataclass, field
from src.parse.model.tim import TIM
from src.parse.model.model_data import ModelData
from src.parse.headers.model_header import ModelHeader
from src.parse.mch.mch_header import MCHHeader
from typing import List

@dataclass
class ModelParser:
  header: ModelHeader
  model_data: ModelData = field(init=False)
  textures: List[TIM] = field(init=False)
  successful_tim_offset: int | None = field(init=False, default=None)

  def __init__(self, header: ModelHeader, data: bytes, mch_model_file_path: str, previous_tim_offset: int | None = None):
    self.header = header
    self.previous_tim_offset = previous_tim_offset

    if header.is_main_field_model:
      self.parse_main_character_model(
        mch_model_file_path=mch_model_file_path,
        char_one_data=data[header.model_offset + 4:],
      )
    else:
      self.parse_non_main_character_model(data)

  def parse_main_character_model(self, mch_model_file_path: str, char_one_data: bytes):
    with open(mch_model_file_path, "rb") as f:
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
    print(f"TIM offsets for model {self.header.model_name}: {tim_offsets}")
    
    self.textures = self.parse_textures(data, tim_offsets)
    print(f"Parsed {len(self.textures)} textures for model {self.header.model_name}")
    if len(self.textures) == 0 and self.previous_tim_offset is not None:
      print(f"Using previous TIM offset {self.previous_tim_offset} for model {self.header.model_name}")
      self.textures = self.parse_textures(data, [self.previous_tim_offset])
      self.successful_tim_offset = self.previous_tim_offset
    else:
      self.successful_tim_offset = tim_offsets[0] if len(tim_offsets) > 0 else None

  def parse_textures(self, data: bytes, offsets: List[int]):
    textures: List[TIM] = []

    for offset in offsets:
      if offset > len(data):
        print(f"Offset {offset} is greater than data length {len(data)}")
        continue

      try:
        tim = TIM(
          name=self.header.model_name,
          data=data[offset:]
        )

        textures.append(tim)
      except ValueError as e:
        print(f"!!! Failed to parse TIM at offset {offset} for model {self.header.model_name}: {e}. Offset is invalid", offset)
    
    return textures
