from dataclasses import dataclass
from typing import List, Dict, Optional
from src.format.animations.formatted_animation import FormattedAnimation
from ..format.animations.root_bone_pose import RootBonePose
from .types import BoneData
import math
from mathutils import Euler

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
    rotation: List[float]  # [y, x, z] in radians
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
    
    def __init__(self, formatted_animation: FormattedAnimation, bones: List[BoneData]):
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

    def get_rest_pose_rotation(self, bone_name: str, rotation: List[float]) -> List[float]:
        # Create Euler from rotation in YXZ order
        eul = Euler((rotation[1], rotation[0], rotation[2]), 'YXZ')
        
        # Apply special rotations based on bone name
        if(bone_name=="upperbody"):
            eul.rotate_axis('Y',math.radians(-85))
        if(bone_name=="lowerbody"):
            if rotation[0] > 0:
                eul.rotate_axis('Y',math.radians(-90))
            else:
                eul.rotate_axis('Y',math.radians(90))
        if bone_name == "neck":
            eul.rotate_axis('Y', math.radians(180))
        elif bone_name == "head":
            eul.rotate_axis('Y', math.radians(170))
        elif bone_name == "hair0":
            eul.rotate_axis('Y', math.radians(150))
        elif bone_name == "hair1" or bone_name == "hair2":
            eul.y = 0
        elif bone_name == "hair3":
            eul.rotate_axis('Y', math.radians(-45))
        elif bone_name == "collar0" or bone_name == "collar2":
            eul.x = 0
            eul.rotate_axis('Z', math.radians(-30))
            eul.rotate_axis('Y', math.radians(-90))
        elif bone_name == "collar1":
            eul.x = 0
            eul.rotate_axis('X', math.radians(90))
            eul.rotate_axis('Y', math.radians(30))
        elif bone_name == "collar3":
            eul.x = 0
            eul.rotate_axis('X', math.radians(-90))
            eul.rotate_axis('Y', math.radians(30))
        elif bone_name == "cape0" or bone_name == "cape1":
            eul.x = 0
            eul.y = 0
            eul.z = 0
            eul.rotate_axis('Y', math.radians(-20))
        elif bone_name == "cape3":
            eul.x = 0
        elif bone_name == "cape4":
            eul.x = 0
            eul.y = 0
            eul.z = 0
        elif bone_name == "dress1" or bone_name == "dress4":
            eul.rotate_axis('Y',math.radians(90))
            eul.rotate_axis('Z',math.radians(90))
        elif bone_name == "dress0" or bone_name == "dress3":
            eul.z = 0
            eul.y = 0
            eul.x = 0
        elif bone_name == "dress2" or bone_name == "dress5":
            eul.z = 0
        elif bone_name == "belt0":
            eul.rotate_axis('Y', math.radians(100))
            eul.rotate_axis('X', math.radians(-10))
        elif bone_name == "belt1":
            eul.rotate_axis('Y', math.radians(100))
            eul.rotate_axis('X', math.radians(10))
        elif bone_name == "belt2":
            eul.rotate_axis('Z', math.radians(30))
            eul.rotate_axis('Y', math.radians(120))
        elif bone_name == "belt4":
            eul.rotate_axis('Z', math.radians(-30))
            eul.rotate_axis('Y', math.radians(120))
        elif bone_name == "belt3":
            eul.rotate_axis('Y', math.radians(90))
            eul.rotate_axis('Z', math.radians(-45))
        elif bone_name == "belt5":
            eul.rotate_axis('Y', math.radians(90))
            eul.rotate_axis('Z', math.radians(45))
        elif bone_name == "breast_R":
            eul.rotate_axis('Y', math.radians(45))
            eul.rotate_axis('X', math.radians(-10))
        elif bone_name == "breast_L":
            eul.rotate_axis('Y', math.radians(45))
            eul.rotate_axis('X', math.radians(10))
            eul.rotate_axis('Z', math.radians(180))
        elif bone_name == "shoulder_R":
            eul.rotate_axis('Y', math.radians(45))
            eul.rotate_axis('Z', math.radians(70))
            eul.rotate_axis('X', math.radians(15))
        elif bone_name == "shoulder_L":
            eul.rotate_axis('Y', math.radians(45))
            eul.rotate_axis('Z', math.radians(-70))
            eul.rotate_axis('X', math.radians(-15))
        elif bone_name == "hip_R" or bone_name == "hip_L":
            eul.y = 0
            eul.z = 0
            eul.rotate_axis('Y', math.radians(-20))
        elif bone_name == "thigh_R" or bone_name == "thigh_L":
            eul.x = 0
            eul.y = 0
            eul.z = 0
            
        # Return in YXZ order
        return [eul.y, eul.x, eul.z]

    def get_keyframe_rotation(self, bone_name: str, rotation: List[float]) -> List[float]:
        # Create Euler from rotation in YXZ order
        eul = Euler((rotation[1], rotation[0], rotation[2]), 'YXZ')
        
        # Apply special rotations based on bone name
        if bone_name == "breast_R" or bone_name == "breast_L":
            eul.rotate_axis('Y', math.radians(180))
        elif bone_name in ["belt0", "belt1", "belt2", "belt4"]:
            eul.rotate_axis('Y', math.radians(180))
        elif bone_name == "belt5":
            eul.rotate_axis('X', math.radians(90))
        elif bone_name in ["dress1", "dress4"]:
            eul.rotate_axis('Z', math.radians(90))
        elif bone_name == "cape3":
            eul.rotate_axis('Y', math.radians(180))
        elif bone_name == "hair5":
            eul.rotate_axis('Y', math.radians(180))
        elif bone_name in ["collar0", "collar2"]:
            eul.rotate_axis('Y', math.radians(180))
            
        # Return in YXZ order
        return [eul.y, eul.x, eul.z]

    def construct_keyframes(self, formatted_animation: FormattedAnimation, bones: List[BoneData]) -> List[Keyframe]:
        """Construct keyframes from animation data.
        
        Args:
            formatted_animation: Animation data from MCH format
            bones: List of bone data to get bone names from
            
        Returns:
            List of keyframes with joint transforms
        """
        keyframes: List[Keyframe] = []
        
        for frame_index, frame in enumerate(formatted_animation.frames):
            # Calculate time for this keyframe
            time = frame_index / 30.0  # 30 FPS
            
            # Process each bone pose in the frame
            joint_transforms: List[JointTransform] = []
            
            for bone_index, pose in enumerate(frame.poses):
                if isinstance(pose, RootBonePose):
                    # Root bone has location and rotation
                    rotation = [pose.x, pose.y, pose.z]
                    rotation = self.get_keyframe_rotation("root", rotation)
                    transform = JointTransform(
                        bone_index=bone_index,
                        bone_name=bones[bone_index]["name"],
                        location=pose.location,
                        rotation=rotation
                    )
                else:
                    # Other bones only have rotation
                    rotation = [pose.x, pose.y, pose.z]
                    # Get bone name from skeleton
                    bone_name = bones[bone_index]["name"]
                    rotation = self.get_keyframe_rotation(bone_name, rotation)
                    transform = JointTransform(
                        bone_index=bone_index,
                        bone_name=bone_name,
                        rotation=rotation
                    )
                
                joint_transforms.append(transform)
            
            keyframe = Keyframe(
                time=time,
                joint_transforms=joint_transforms
            )
            keyframes.append(keyframe)
        
        return keyframes

    def __repr__(self) -> str:
        return f"ConstructedAnimation: {self.name} ({self.duration}s, {len(self.keyframes)} keyframes)" 

    def get_rest_pose(self) -> List[Dict[str, float]]:
        """Get the pose data from the first frame of the animation.
        
        Returns:
            List of bone rotations in radians
        """
        if not self.keyframes:
            return []
            
        first_frame = self.keyframes[0]
        rotations: List[Dict[str, float]] = []
        
        for transform in first_frame.joint_transforms:
            # Get base rotation from first frame
            base_rotation = transform.rotation
            
            # Apply special rotations on top of base rotation
            final_rotation = self.get_rest_pose_rotation(transform.bone_name, base_rotation)
            
            rotations.append({
                "rotX": final_rotation[0],
                "rotY": final_rotation[1],
                "rotZ": final_rotation[2]
            })
            
        return rotations 