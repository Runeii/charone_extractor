from io import BytesIO
from ...utils.binary_reader import BinaryReader
from dataclasses import dataclass, field

@dataclass(init=False)
class MCHHeader:
  tim_offsets: list[int]
  model_data_offset: int = field(init=False)

  def __init__(self, data: bytes):
    if len(data) != 256:
        raise ValueError(f"Expected 256 bytes, got {len(data)} bytes")
    
    stream = BytesIO(data)

    self.tim_offsets = []

    while True:
      offset = BinaryReader.read_uint32(stream)
      if offset == 4294967295: 
        break
      
      self.tim_offsets.append(offset)
    
    self.model_data_offset = BinaryReader.read_uint32(stream)