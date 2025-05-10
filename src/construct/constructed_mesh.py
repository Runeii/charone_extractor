from dataclasses import dataclass
from typing import List, Dict, Any
from ..format.formatted_face import FormattedFace
from ..format.formatted_vertex import FormattedVertex
from ..format.formatted_skin import FormattedSkin

@dataclass(init=False)
class ConstructedMesh:
    vertices: List[Dict[str, float]]  # List of {x, y, z} positions
    normals: List[Dict[str, float]]   # List of {x, y, z} normals
    uvs: List[Dict[str, float]]       # List of {u, v} coordinates
    indices: List[int]                # Triangle indices
    weights: List[Dict[str, Any]]     # List of {joints: [indices], weights: [values]}
    
    def __init__(self, formatted_faces: List[FormattedFace], 
                 formatted_vertices: List[FormattedVertex],
                 skin_objects: List[FormattedSkin]):
        self.vertices = self.construct_vertices(formatted_vertices)
        self.normals = self.construct_normals(formatted_faces)
        self.uvs = self.construct_uvs(formatted_faces)
        self.indices = self.construct_indices(formatted_faces)
        self.weights = self.construct_weights(formatted_vertices, skin_objects)

    def construct_vertices(self, formatted_vertices: List[FormattedVertex]) -> List[Dict[str, float]]:
        return [{"x": v.x, "y": v.y, "z": v.z} for v in formatted_vertices]

    def construct_normals(self, formatted_faces: List[FormattedFace]) -> List[Dict[str, float]]:
        # TODO: Implement normal calculation
        return []

    def construct_uvs(self, formatted_faces: List[FormattedFace]) -> List[Dict[str, float]]:
        uvs = []
        for face in formatted_faces:
            for coords in face.texture_coords:
                uvs.append({
                    "u": coords[0],
                    "v": coords[1]
                })
        return uvs

    def construct_indices(self, formatted_faces: List[FormattedFace]) -> List[int]:
        # TODO: Implement triangle index construction
        return []

    def construct_weights(self, formatted_vertices: List[FormattedVertex], 
                         skin_objects: List[FormattedSkin]) -> List[Dict[str, Any]]:
        # TODO: Implement weight construction from skin objects
        return []

    def __repr__(self) -> str:
        return f"ConstructedMesh: {len(self.vertices)} vertices, {len(self.indices)//3} triangles" 