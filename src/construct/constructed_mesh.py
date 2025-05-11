from dataclasses import dataclass
from typing import List, Dict
from src.format.formatted_face import FormattedFace
from src.format.formatted_vertex import FormattedVertex
from src.format.formatted_skin import FormattedSkin
from src.construct.constructed_skeleton import ConstructedSkeleton
import math

@dataclass(init=False)
class ConstructedMesh:
    vertices: List[Dict[str, float]]  # List of {x, y, z} positions
    uvs: List[Dict[str, float]]       # List of {u, v} coordinates
    indices: List[int]                # Triangle indices
    
    def __init__(self, formatted_faces: List[FormattedFace], 
                 formatted_vertices: List[FormattedVertex],
                 skeleton: ConstructedSkeleton):
        # First construct vertices in order of skin groups
        self.vertices = self.construct_vertices(formatted_vertices, skeleton.skins)
        self.uvs = self.construct_uvs(formatted_faces)
        self.indices = self.construct_indices(formatted_faces)

    def construct_vertices(self, formatted_vertices: List[FormattedVertex], skins: List[FormattedSkin]) -> List[Dict[str, float]]:
        """Construct vertices from MCH format data, ordered by skin groups.
        
        Args:
            formatted_vertices: List of vertices from MCH format
            skins: List of skin objects defining vertex groups
            
        Returns:
            List of vertex positions ordered by skin groups
        """
        # Create a list to store reordered vertices
        reordered_vertices = []
        
        # Process each skin group
        for skin in skins:
            # Get vertices for this skin group
            for i in range(skin.vertex_count):
                vertex_idx = skin.first_vertex_index + i
                if vertex_idx < len(formatted_vertices):
                    vertex = formatted_vertices[vertex_idx]
                    reordered_vertices.append({"x": vertex.x, "y": vertex.y, "z": vertex.z})
        
        return reordered_vertices

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

    def __repr__(self) -> str:
        return f"ConstructedMesh: {len(self.vertices)} vertices, {len(self.indices)//3} triangles" 