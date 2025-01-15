import struct
from dataclasses import dataclass
from typing import List, Tuple
import logging
from io import BytesIO
from .tim import TIM
from .model_data import ModelData

class Model:
    def __init__(self, id: int, name: str, model_offset: int, tim_offsets: int, data_offset: int, data: bytes):
        self.id = id
        self.name = name.replace('HXh', '')
        self.tim_offset = tim_offsets[0] if tim_offsets else False
        self.model_offset = model_offset
        self.data_offset = data_offset
        self.data = data
        self.tim = None

        self.model_data = ModelData(self.name, self.data, self.model_offset + self.data_offset + 4)

        return
        # Note: need to +4 for PC files
        self.tim = TIM(self.name, self.data[self.model_offset + self.tim_offset + 4:]) if self.tim_offset is not None else None

        if self.tim:
          self.tim.save("output/" + self.name)
    
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