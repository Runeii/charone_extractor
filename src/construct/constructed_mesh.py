from dataclasses import dataclass
from typing import List, Dict
from ..format.formatted_face import FormattedFace
from ..format.formatted_vertex import FormattedVertex
from ..format.formatted_skin import FormattedSkin
import math

@dataclass(init=False)
class ConstructedMesh:
    vertices: List[Dict[str, float]]  # List of {x, y, z} positions
    uvs: List[Dict[str, float]]       # List of {u, v} coordinates
    indices: List[int]                # Triangle indices
    weights: List[Dict[int, float]]   # List of {joints: [indices], weights: [values]}
    
    def __init__(self, formatted_faces: List[FormattedFace], 
                 formatted_vertices: List[FormattedVertex],
                 skin_objects: List[FormattedSkin]):
        self.vertices = self.construct_vertices(formatted_vertices)
        self.uvs = self.construct_uvs(formatted_faces)
        self.indices = self.construct_indices(formatted_faces)
        self.weights = self.construct_weights(formatted_faces, skin_objects)

    def construct_vertices(self, formatted_vertices: List[FormattedVertex]) -> List[Dict[str, float]]:
        return [{"x": v.x, "y": v.y, "z": v.z} for v in formatted_vertices]

    def _calculate_uv(self, u: int, v: int, tgroup: List[int]) -> Dict[str, float]:
        """Calculate UV coordinates with texture group offsets and scaling."""
        return {
            "u": (u + tgroup[0] * 128) / 128,
            "v": ((128 - v) + tgroup[1] * 128) / 128
        }

    def construct_uvs(self, formatted_faces: List[FormattedFace]) -> List[Dict[str, float]]:
        uvs: List[Dict[str, float]] = []
        for face in formatted_faces:
            # Calculate texture group
            tgroup = [math.floor(face.texture_index/2), face.texture_index%2]
            
            # Process UVs in correct order: v2, v1, v3, v4
            coords = face.texture_coords
            if len(coords) >= 3:  # At least a triangle
                # Add UVs in v2, v1, v3 order
                uvs.extend([
                    self._calculate_uv(coords[0][0], coords[0][1], tgroup),  # v2
                    self._calculate_uv(coords[1][0], coords[1][1], tgroup),  # v1
                    self._calculate_uv(coords[2][0], coords[2][1], tgroup),  # v3
                ])
                
                # Add v4 if quad
                if len(coords) == 4:
                    uvs.append(self._calculate_uv(coords[3][0], coords[3][1], tgroup))
                    
        return uvs

    def construct_indices(self, formatted_faces: List[FormattedFace]) -> List[int]:
      indices: List[int] = []
      for face in formatted_faces:
        if face.v4 is None:
          indices.extend([face.v1, face.v2, face.v3])
        else:
          indices.extend([face.v1, face.v2, face.v3])
          indices.extend([face.v1, face.v3, face.v4])
      return indices

    def construct_weights(self, formatted_faces: List[FormattedFace], formatted_skins: List[FormattedSkin]) -> List[Dict[int, float]]:
      weights: List[Dict[int, float]] = [{} for _ in range(len(self.vertices))]
      
      for skin in formatted_skins:
        for vertex_idx in range(skin.first_vertex_index, skin.first_vertex_index + skin.vertex_count):
          if vertex_idx < len(weights):
            weights[vertex_idx] = {skin.bone_id: 1.0}
    
      return weights

    def __repr__(self) -> str:
        return f"ConstructedMesh: {len(self.vertices)} vertices, {len(self.indices)//3} triangles" 