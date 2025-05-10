from dataclasses import dataclass
from typing import List, Dict, Any
from ..formatted_bone import FormattedBone
from ..parse.model.skin_object import SkinObject

@dataclass(init=False)
class ConstructedSkeleton:
    joints: List[Dict[str, Any]]  # List of {name, parent, transform}
    inverse_bind_matrices: List[List[float]]  # List of 4x4 matrices
    vertex_bone_mappings: List[Dict[str, Any]]  # List of {joints: [indices], weights: [values]}
    
    def __init__(self, formatted_bones: List[FormattedBone], skin_objects: List[SkinObject], vertex_count: int):
        self.joints = self.construct_joints(formatted_bones)
        self.vertex_bone_mappings = self.construct_vertex_bone_mappings(skin_objects, vertex_count)
        self.inverse_bind_matrices = self.construct_inverse_bind_matrices(formatted_bones)

    def construct_joints(self, formatted_bones: List[FormattedBone]) -> List[Dict[str, Any]]:
        joints = []
        for bone in formatted_bones:
            joint = {
                "name": f"bone_{bone.bone}",
                "parent": bone.parent_bone if bone.parent_bone != -1 else None,
                "transform": self.calculate_joint_transform(bone)
            }
            joints.append(joint)
        return joints

    def construct_vertex_bone_mappings(self, skin_objects: List[SkinObject], vertex_count: int) -> List[Dict[str, Any]]:
        # Initialize mappings for all vertices
        mappings = [{"joints": [], "weights": []} for _ in range(vertex_count)]
        
        # Process each skin object to build the mappings
        for skin in skin_objects:
            for vertex_index, bone_indices, weights in zip(skin.vertex_indices, skin.bone_indices, skin.weights):
                mappings[vertex_index] = {
                    "joints": bone_indices,
                    "weights": weights
                }
        
        return mappings

    def calculate_joint_transform(self, bone: FormattedBone) -> List[float]:
        # TODO: Implement joint transform calculation
        # Should return a 4x4 matrix as a flat list
        return [1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0]

    def construct_inverse_bind_matrices(self, formatted_bones: List[FormattedBone]) -> List[List[float]]:
        # TODO: Implement inverse bind matrix calculation using vertex_bone_mappings
        return []

    def __repr__(self) -> str:
        return f"ConstructedSkeleton: {len(self.joints)} joints, {len(self.vertex_bone_mappings)} vertex mappings" 