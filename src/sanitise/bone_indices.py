from dataclasses import dataclass, field
from typing import List
from .sanitised_vertex import SanitisedVertex
from ..parse.model.skin_object import SkinObject

@dataclass
class BoneIndices:
  """Manages the mapping between vertices and their controlling bones.
  Each vertex is controlled by exactly one bone with an implicit weight of 1.0."""
  
  vertices: List[SanitisedVertex]
  skin_objects: List[SkinObject]
  indices: List[int] = field(init=False)

  def __post_init__(self):
    """Builds the vertex-to-bone mapping on initialization."""
    # Initialize all vertices to None to catch any unmapped vertices
    self.indices = [None] * len(self.vertices)
    
    # Map each vertex to its controlling bone
    for skin in self.skin_objects:
      start = skin.first_vertex_index
      end = start + skin.vertex_count
      
      for vertex_idx in range(start, end):
        self.indices[vertex_idx] = skin.bone_id