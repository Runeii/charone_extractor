from dataclasses import dataclass
from typing import List
from src.format.formatted_model import FormattedModel
from .constructed_mesh import ConstructedMesh
from .constructed_skeleton import ConstructedSkeleton
from .constructed_animation import ConstructedAnimation

@dataclass(init=False)
class ConstructedModel:
    name: str
    meshes: List[ConstructedMesh]
    skeleton: ConstructedSkeleton
    animations: List[ConstructedAnimation]
    
    def __init__(self, formatted_model: FormattedModel):
        self.name = formatted_model.name
        self.meshes = self.construct_meshes(formatted_model)
        self.skeleton = self.construct_skeleton(formatted_model)
        self.animations = self.construct_animations(formatted_model)

    def construct_meshes(self, formatted_model: FormattedModel) -> List[ConstructedMesh]:
        return [ConstructedMesh(
            formatted_faces=formatted_model.faces,
            formatted_vertices=formatted_model.vertices,
            skin_objects=formatted_model.skin_objects
        )]

    def construct_skeleton(self, formatted_model: FormattedModel) -> ConstructedSkeleton:
        rest_pose_data = None
            
        return ConstructedSkeleton(
            formatted_bones=formatted_model.bones,
            formatted_skins=formatted_model.skin_objects,
            rest_pose_data=rest_pose_data
        )

    def construct_animations(self, formatted_model: FormattedModel) -> List[ConstructedAnimation]:
        return [ConstructedAnimation(formatted_animation=animation, bones=self.skeleton.bones) for animation in formatted_model.animations]

    def __repr__(self) -> str:
        return f"ConstructedModel: {self.name}\n" 