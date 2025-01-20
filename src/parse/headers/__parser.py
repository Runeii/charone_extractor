from dataclasses import dataclass
from typing import List
from ...utils.binary_reader import BinaryReader
from io import BytesIO
from .model_header import ModelHeader

@dataclass(init=False)
class HeaderParser:
  model_count: int
  model_headers: List[ModelHeader]

  def __init__(self, file_data: bytes):
      if len(file_data) < 0x800:
          print(f"File too short: {len(file_data)} bytes")
          return []

      stream = BytesIO(file_data)

      self.model_count = BinaryReader.read_uint32(stream)

      self.model_headers = self.parse_model_headers(file_data, self.model_count, 4)
    
  def parse_model_headers(self, data: bytes, model_count: int, offset: int):
    stream = BytesIO(data[4:])
    model_headers = []

    for i in range(model_count):
      model_header = ModelHeader(stream)
      model_headers.append(model_header)
    
    return model_headers