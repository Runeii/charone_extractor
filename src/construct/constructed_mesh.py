from dataclasses import dataclass
from typing import List, Dict, Tuple
from src.format.formatted_face import FormattedFace
from src.format.formatted_vertex import FormattedVertex
from src.format.formatted_skin import FormattedSkin
from src.construct.constructed_skeleton import ConstructedSkeleton
import math
from src.parse.model.mesh import Mesh

@dataclass(init=False)
class ConstructedMesh:
    vertices: List[Dict[str, float]] 
    uvs: List[Dict[str, float]]
    faces: List[List[int]]
    formatted_faces: List[FormattedFace]  # Store original formatted faces for UV mapping
    
    def __init__(self,
                 mesh: Mesh,
                 faces_start_offset: int,
                 formatted_faces: List[FormattedFace], 
                 formatted_vertices: List[FormattedVertex],
                 skeleton: ConstructedSkeleton):

        filtered_vertices = formatted_vertices
        filtered_faces = formatted_faces[faces_start_offset:faces_start_offset + mesh.triangle_count + mesh.quad_count]
        filtered_skins = skeleton.skins[mesh.skinobject_start:mesh.skinobject_start + mesh.skinobject_count]

        self.vertices = self.construct_vertices(filtered_vertices, filtered_skins)
        self.uvs = self.construct_uvs(filtered_faces)
        self.faces = self.construct_faces(filtered_faces)
        self.formatted_faces = filtered_faces  # Store the original formatted faces

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
                    reordered_vertices.append({
                        "x": vertex.x,
                        "y": vertex.z,
                        "z": vertex.y
                    })
        
        return reordered_vertices

    def _calculate_uv(self, u: int, v: int, tgroup: List[int]) -> Dict[str, float]:
        """Calculate UV coordinates with texture group offsets and scaling."""
        v = 128 - v
        # Apply texture group offset first
        u += tgroup[0] * 128
        v += tgroup[1] * 128
        
        # Scale coordinates
        return {
            "u": u / 128,
            "v": v / 128
        }

    def construct_uvs(self, formatted_faces: List[FormattedFace]) -> List[Dict[str, float]]:
        # First pass: collect all UVs
        all_uvs: List[Dict[str, float]] = []
        for face in formatted_faces:
            # Calculate texture group
            tgroup = [math.floor(face.texture_index/2), face.texture_index%2]
            
            # Process UVs in correct order: v2, v1, v3, v4
            coords = face.texture_coords
            if len(coords) >= 3:
                all_uvs.extend([
                    self._calculate_uv(coords[0][0], coords[0][1], tgroup),  # v2
                    self._calculate_uv(coords[1][0], coords[1][1], tgroup),  # v1
                    self._calculate_uv(coords[2][0], coords[2][1], tgroup),  # v3
                ])
                
                # Add v4 if quad
                if len(coords) == 4:
                    all_uvs.append(self._calculate_uv(coords[3][0], coords[3][1], tgroup))

        # Second pass: deduplicate UVs and set indices
        unique_uvs: List[Dict[str, float]] = []
        uv_indices: Dict[Tuple[float, float], int] = {}  # (u,v) -> index mapping
        
        for face in formatted_faces:
            coords = face.texture_coords
            if len(coords) >= 3:
                # Process v2
                uv = self._calculate_uv(coords[0][0], coords[0][1], [math.floor(face.texture_index/2), face.texture_index%2])
                key = (uv["u"], uv["v"])
                if key not in uv_indices:
                    uv_indices[key] = len(unique_uvs)
                    unique_uvs.append(uv)
                face.vt2 = uv_indices[key]
                
                # Process v1
                uv = self._calculate_uv(coords[1][0], coords[1][1], [math.floor(face.texture_index/2), face.texture_index%2])
                key = (uv["u"], uv["v"])
                if key not in uv_indices:
                    uv_indices[key] = len(unique_uvs)
                    unique_uvs.append(uv)
                face.vt1 = uv_indices[key]
                
                # Process v3
                uv = self._calculate_uv(coords[2][0], coords[2][1], [math.floor(face.texture_index/2), face.texture_index%2])
                key = (uv["u"], uv["v"])
                if key not in uv_indices:
                    uv_indices[key] = len(unique_uvs)
                    unique_uvs.append(uv)
                face.vt3 = uv_indices[key]
                
                # Process v4 if quad
                if len(coords) == 4:
                    uv = self._calculate_uv(coords[3][0], coords[3][1], [math.floor(face.texture_index/2), face.texture_index%2])
                    key = (uv["u"], uv["v"])
                    if key not in uv_indices:
                        uv_indices[key] = len(unique_uvs)
                        unique_uvs.append(uv)
                    face.vt4 = uv_indices[key]

        return unique_uvs

    def construct_faces(self, formatted_faces: List[FormattedFace]) -> List[List[int]]:
        faces: List[List[int]] = []
        for face in formatted_faces:
          if face.is_triangle:
              faces.append([face.v1, face.v2, face.v3])
          elif face.v4 is not None:
              faces.append([face.v1, face.v2, face.v3, face.v4])
        return faces

    def __repr__(self) -> str:
        return f"ConstructedMesh: {len(self.vertices)} vertices, {len(self.faces)} faces" 