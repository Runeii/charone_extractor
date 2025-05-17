from dataclasses import dataclass
from typing import List, Dict, Optional
from src.format.animations.formatted_animation import FormattedAnimation
from ..format.animations.root_bone_pose import RootBonePose
import math
from mathutils import Euler
from .constructed_bone import ConstructedBone
@dataclass
class JointTransform:
    """Represents a single joint/bone transform in a keyframe.
    
    Attributes:
        bone_index: Index of the bone in the skeleton
        bone_name: Name of the bone
        location: Optional location [x, y, z] for root bone
        rotation: Rotation [x, y, z] in radians in YXZ order
    """
    bone_index: int
    bone_name: str
    rotation: List[float]
    location: Optional[List[float]] = None

@dataclass
class Keyframe:
    """Represents a single keyframe in the animation.
    
    Attributes:
        time: Time in seconds when this keyframe occurs
        joint_transforms: List of joint transforms for this keyframe
    """
    time: float
    joint_transforms: List[JointTransform]

@dataclass(init=False)
class ConstructedAnimation:
    """Constructs animation data from MCH format for Blender import.
    
    Attributes:
        name: Name of the animation
        duration: Duration of the animation in seconds
        keyframes: List of keyframes containing joint transforms
    """
    name: str
    duration: float
    keyframes: List[Keyframe]
    
    def __init__(self, formatted_animation: FormattedAnimation, bones: List[ConstructedBone]):
        """Initialize animation from formatted data.
        
        Args:
            formatted_animation: Animation data from MCH format
            bones: List of bone data to get bone names from
        """
        self.name = formatted_animation.name
        self.duration = self.calculate_duration(formatted_animation)
        self.keyframes = self.construct_keyframes(formatted_animation, bones)

    def calculate_duration(self, formatted_animation: FormattedAnimation) -> float:
        """Calculate animation duration in seconds.
        
        Args:
            formatted_animation: Animation data from MCH format
            
        Returns:
            Duration in seconds
        """
        # Each frame represents 1/30th of a second in FF8
        return formatted_animation.frame_count / 30.0

    def construct_keyframes(self, formatted_animation: FormattedAnimation, bones: List[ConstructedBone]) -> List[Keyframe]:
        """Construct keyframes from animation data.
        
        Args:
            formatted_animation: Animation data from MCH format
            bones: List of bone data to get bone names from
            
        Returns:
            List of keyframes with joint transforms
        """
        keyframes: List[Keyframe] = []
        
        for frame_index, frame in enumerate(formatted_animation.frames):
            time = frame_index / 30.0
            
            joint_transforms: List[JointTransform] = []

            for bone_index, pose in enumerate(frame.poses):
                rotation = [pose.x, pose.y, pose.z]
                rotation = self.get_keyframe_rotation(bones[bone_index].name, rotation)

                #TODO: fix this to be accurate for root bone, but 0 is fine for now
                location = [0.0, 0.0, 0.0]

                transform = JointTransform(
                    bone_index=bone_index,
                    bone_name=bones[bone_index].name,
                    location=location,
                    rotation=rotation
                )
                
                joint_transforms.append(transform)
            
            keyframe = Keyframe(
                time=time,
                joint_transforms=joint_transforms
            )
            keyframes.append(keyframe)
        
        return keyframes

    def get_keyframe_rotation(self, bone_name: str, rotation: List[float]) -> List[float]:
        eul = Euler((-rotation[0], -rotation[1], rotation[2]), 'YXZ')

        # Apply special rotations based on bone name
        if bone_name == "root":
            eul=Euler((0,0,0), 'YXZ')
        if bone_name == "upperbody":
            eul.rotate(Euler((math.radians(180), 0, 0), 'YXZ'))
            eul.rotate(Euler((0, 0, math.radians(-90)), 'YXZ'))
        if bone_name == "lowerbody":
            eul.rotate(Euler((0, 0, math.radians(-90)), 'YXZ'))
        elif bone_name == "breast_R" or bone_name == "breast_L":
            eul.rotate(   Euler  ((0,math.radians(180),0), 'YXZ'))
        elif bone_name in ["belt0", "belt1", "belt2", "belt4"]:
            eul.rotate(Euler((0, math.radians(180), 0), 'YXZ'))
        elif bone_name == "belt5":
            eul.rotate(Euler((math.radians(90), 0, 0), 'YXZ'))
        elif bone_name in ["dress1", "dress4"]:
            eul.rotate(Euler((0, 0, math.radians(90)), 'YXZ'))
        elif bone_name == "cape3":
            eul.rotate(Euler((0, math.radians(180), 0), 'YXZ'))
        elif bone_name == "hair5":
            eul.rotate(Euler((0, math.radians(180), 0), 'YXZ'))
        elif bone_name in ["collar0", "collar2"]:
            eul.rotate(Euler((0, math.radians(180), 0), 'YXZ'))
        
        return [eul.x, eul.y, eul.z]

    def __repr__(self) -> str:
        return f"ConstructedAnimation: {self.name} ({self.duration}s, {len(self.keyframes)} keyframes)" 
