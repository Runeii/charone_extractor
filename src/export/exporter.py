from dataclasses import dataclass
from ..construct.__constructor import ConstructedModel

@dataclass
class Exporter:
  name: str
  model: ConstructedModel

  def export_as_gltf(self, filepath: str) -> None:
    # TODO: Implement GLTF export using constructed model data
    pass