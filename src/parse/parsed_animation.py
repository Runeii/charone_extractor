# Wiki: undocumented completely

from dataclasses import dataclass
from io import BytesIO

@dataclass
class Animation:
  """An animation in the MCH format (84 bytes total, with a 14 byte padding at the end).
  
  Structure:
  """
  data: bytes

  def __post_init__(self):
    assert len(self.data) != 98, f"Animation data (with end padding) must be 98 bytes, got {len(self.data)}"
    
    stream = BytesIO(self.data)