from dataclasses import dataclass
from typing import List, Dict, Any
from ..formatted_bone import FormattedBone

@dataclass(init=False)
class ConstructedSkeleton:
    joints: List[Dict[str, Any]]  # List of {name, parent, transform}
    inverse_bind_matrices: List[List[float]]  # List of 4x4 matrices
    
    def __init__(self, formatted_bones: List[FormattedBone]):
        self.joints = self.construct_joints(formatted_bones)
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

    def calculate_joint_transform(self, bone: FormattedBone) -> List[float]:
        # TODO: Implement joint transform calculation
        # Should return a 4x4 matrix as a flat list
        return [1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0]

    def construct_inverse_bind_matrices(self, formatted_bones: List[FormattedBone]) -> List[List[float]]:
        # TODO: Implement inverse bind matrix calculation
        return []

    def __repr__(self) -> str:
        return f"ConstructedSkeleton: {len(self.joints)} joints" 