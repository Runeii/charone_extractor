from dataclasses import dataclass
from typing import List
from ..parse.model.skin_object import SkinObject

@dataclass(init=False)
class BoneIndices:
  """Manages the mapping between vertices and their controlling bones.
  Each vertex is controlled by exactly one bone with an implicit weight of 1.0."""

  indices: List[int]

  def __init__(self, skin_objects: List[SkinObject], vertex_count: int):
    """Builds the vertex-to-bone mapping on initialization."""
    # Initialize all vertices to None to catch any unmapped vertices
    self.indices = [-1] * vertex_count

    # Map each vertex to its controlling bone
    for skin in skin_objects:
      start = skin.first_vertex_index
      end = start + skin.vertex_count
      
      for vertex_idx in range(start, end):
        self.indices[vertex_idx] = skin.bone_id