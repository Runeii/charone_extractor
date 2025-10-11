from dataclasses import dataclass, field
from typing import List
from src.utils.binary_reader import BinaryReader
from io import BytesIO

@dataclass(init=False)
class ModelHeader:
  model_offset: int = field(init=False)
  data_size: int = field(init=False)
  model_id: int = field(init=False)
  unknown: int = field(init=False)

  is_main_field_model: bool = field(init=False)
  main_field_id: int = field(init=False)

  tim_offsets: List[int] = field(default_factory=list)
  model_data_offset: int = field(init=False)
  model_name: str = field(init=False)

  def __init__(self, stream: BytesIO):
    self.model_offset = BinaryReader.read_uint32(stream)
    self.data_size = BinaryReader.read_uint32(stream)
    flags = BinaryReader.read_uint32(stream)
  
    ## Sometimes there is a duplicate data size field
    if self.data_size == flags:
      flags = BinaryReader.read_uint32(stream)
    
    self.model_id = flags & 0xFF
    _ = (flags >> 8) & 0xFF
    self.unknown = (flags >> 16) & 0xFF
    self.is_main_field_model = (flags >> 24) & 0xFF == 208

    self.tim_offsets = []

    if self.is_main_field_model:
      _main_model_spacer = BinaryReader.read_uint32(stream)
    else:
      self.tim_offsets.append(0)
      while stream.tell() < 0x800:
        tim_offset = BinaryReader.read_uint32(stream)
        if tim_offset == 0xFFFFFFFF:
          break
        
        if tim_offset < self.data_size:
          self.tim_offsets.append(tim_offset);
          continue

        lower_uint16 = tim_offset & 0xFFFF
        self.tim_offsets.append(lower_uint16)
      
      self.model_data_offset = BinaryReader.read_uint32(stream)
    
    string_bytes = BinaryReader.read_bytes(stream, 8)
    self.model_name = string_bytes.decode('ascii', errors='ignore').rstrip('\x00').strip()[:4]
    _spacer2 = BinaryReader.read_uint32(stream)