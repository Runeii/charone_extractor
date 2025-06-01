from dataclasses import dataclass
from typing import List
import string
from src.utils.binary_reader import BinaryReader
from io import BytesIO
from .model_header import ModelHeader

@dataclass(init=False)
class HeaderParser:
  model_count: int
  model_headers: List[ModelHeader]

  def __init__(self, file_data: bytes):
      if len(file_data) < 0x800:
          print(f"File too short: {len(file_data)} bytes")
          self.model_count = 0
          return None

      stream = BytesIO(file_data)

      self.model_count = BinaryReader.read_uint32(stream)
      
      if self.model_count > 255:
        print("Red flag! Model count is greater than 255, this may be one of the old (demo?) format files")
        self.model_count = 0
        return None

      self.model_headers = self.parse_model_headers(file_data, self.model_count, 4)
    
  def parse_model_headers(self, data: bytes, model_count: int, offset: int) -> List[ModelHeader]:
    stream = BytesIO(data[offset:])
    model_headers: List[ModelHeader] = []

    for _ in range(model_count):
      model_header = ModelHeader(stream)
    
      allowed_chars = string.ascii_letters + string.digits

      if len(model_header.model_name) != 4 or not all(c in allowed_chars for c in model_header.model_name):
        print("Model name is not 4 characters long. This suggests invalid data. Skipping")
        continue
      else:
        print("model header", model_header.model_name)
        model_headers.append(model_header)
    
    return model_headers