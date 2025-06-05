from dataclasses import dataclass
from typing import List
from src.format.formatted_model import FormattedModel
from .constructed_mesh import ConstructedMesh
from .constructed_skeleton import ConstructedSkeleton
from .constructed_animation import ConstructedAnimation, JointTransform
from ..format.animations.root_bone_pose import RootBonePose
from ..format.animations.formatted_animation import FormattedAnimation
from ..parse.model.tim import TIM

@dataclass(init=False)
class ConstructedModel:
    name: str
    meshes: List[ConstructedMesh]
    skeleton: ConstructedSkeleton
    rest_animation: ConstructedAnimation
    animations: List[ConstructedAnimation]
    textures: List[TIM]

    def __init__(self, formatted_model: FormattedModel):
        self.name = formatted_model.name
        self.skeleton = self.construct_skeleton(formatted_model)
        self.meshes = self.construct_meshes(formatted_model)
        self.rest_animation = self.construct_animations([formatted_model.animations[0]], None)[0]
        self.animations = self.construct_animations(formatted_model.animations, self.rest_animation)
        self.textures = formatted_model.textures

    def construct_meshes(self, formatted_model: FormattedModel) -> List[ConstructedMesh]:
        return [ConstructedMesh(
            formatted_faces=formatted_model.faces,
            formatted_vertices=formatted_model.vertices,
            skeleton=self.skeleton
        )]

    def construct_skeleton(self, formatted_model: FormattedModel) -> ConstructedSkeleton:
        return ConstructedSkeleton(formatted_model=formatted_model)

    def construct_animations(self, formatted_animations: List[FormattedAnimation], rest_animation: ConstructedAnimation | None) -> List[ConstructedAnimation]:
        rest_pose_transforms: List[JointTransform] = []
        if rest_animation:
          first_frame_raw_poses = formatted_animations[0].frames[0].poses
          rest_pose_transforms = []
          for bone_index, pose in enumerate(first_frame_raw_poses):
            location = None
            if isinstance(pose, RootBonePose):
              location = pose.location
                
            rest_pose_transforms.append(JointTransform(
              bone_index=bone_index,
              bone_name=self.skeleton.bones[bone_index].name,
              rotation=[pose.x, pose.y, pose.z],
              location=location
            ))
        
        return [ConstructedAnimation(
            formatted_animation=animation,
            bones=self.skeleton.bones,
            rest_pose_transforms=rest_pose_transforms
        ) for animation in formatted_animations]

    def __repr__(self) -> str:
        return f"ConstructedModel: {self.name}\n"