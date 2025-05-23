import struct
from io import BytesIO

class BinaryReader:
  @staticmethod
  def read_uint8(stream: BytesIO) -> int:
    return struct.unpack("<B", stream.read(1))[0]

  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]
  
  @staticmethod
  def read_string(stream: BytesIO, length: int = 8) -> str:
    raw_str = stream.read(length)
    
    # Find the first null terminator
    null_pos = raw_str.find(b'\x00')
    if null_pos != -1:
      raw_str = raw_str[:null_pos]
    
    # If the string is empty after null trimming, return empty string
    if not raw_str:
      return ""
      
    # Try UTF-8 first, then fall back to ASCII
    try:
      result = raw_str.decode('utf-8')
    except UnicodeDecodeError:
      result = raw_str.decode('ascii', errors='ignore')
    
    # Remove any backtick characters and strip whitespace
    return result.replace('`', '').strip()