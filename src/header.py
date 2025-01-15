import struct
from dataclasses import dataclass
from typing import List, Tuple
import logging
from io import BytesIO

class CharacterFileParser:
  def __init__(self, debug: bool = False):
      self.logger = logging.getLogger(__name__)
      if debug:
          logging.basicConfig(level=logging.DEBUG)
      else:
          logging.basicConfig(level=logging.WARNING)
  
  def read_uint32(self, stream: BytesIO) -> int:
      """Read a 32-bit unsigned integer from the stream"""
      value = struct.unpack("<I", stream.read(4))[0]
      #self.logger.debug(f"Read uint32 at offset 0x{stream.tell()-4:04X}: 0x{value:08X}")
      return value
  

  def read_string(self, stream: BytesIO, length: int = 8) -> str:
      """Read a fixed-length string from the stream"""
      raw_str = stream.read(length)
      string = raw_str.split(b'\x00')[0].decode('ascii', errors='ignore')
      return string

  def parse_headers(self, file_data: bytes):
      if len(file_data) < 0x800:
          self.logger.error(f"File too short: {len(file_data)} bytes")
          return []

      stream = BytesIO(file_data)
      models = []
      
      # Read model count
      model_count = self.read_uint32(stream)
      self.logger.debug(f"Model count: {model_count}")
      
      # Process each model section
      for i in range(7):
          model = {}
          
          model_offset = self.read_uint32(stream)
          data_size = self.read_uint32(stream)

          model_id = self.read_uint32(stream)
          if data_size == model_id:
              model_id = self.read_uint32(stream)

          is_main_field_model = model_id >> 24 == 0xd0

          tim_offsets = []
          if is_main_field_model:
              # For main field models, read another model ID which should be 0
              main_field_zero_id = self.read_uint32(stream)
              if main_field_zero_id != 0:
                  self.logger.error(f"Expected 0x00000000 after main field model ID, got 0x{main_field_zero_id:08X}")

          else:
              # Read tim offsets until we hit 0xFFFFFFFF
              if (model_id & 0xFFFFFF) == 0:
                  tim_offsets.append(0)
              
              while stream.tell() < 0x800:
                  tim_offset = self.read_uint32(stream)
                  if tim_offset == 0xFFFFFFFF:
                      break
                  tim_offsets.append(tim_offset)

          model_data_offset = 0
          if is_main_field_model == False:
            model_data_offset = self.read_uint32(stream)
          model_name = self.read_string(stream)

          spacer = self.read_uint32(stream) # real spacer

          model['id'] = model_id
          model['name'] = model_name
          model['model_offset'] = model_offset
          model['tim_offsets'] = tim_offsets
          model['data_offset'] = model_data_offset
          models.append(model)
          
      return models
