from dataclasses import dataclass
from typing import List, Dict, Any
from src.format.animations.formatted_animation import FormattedAnimation
from ..format.animations.root_bone_pose import RootBonePose
from .constructed_skeleton import BoneData

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
    keyframes: List[Dict[str, Any]]  # List of {time, joint_transforms}
    
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

    # ##TODO LATER: Add special bone rotations from other-implementation.py (~1000-1200)
    # - Neck: 180° Y rotation
    # - Head: 170° Y rotation
    # - Hair bones: hair0 (150° Y), hair1/2 (0° Y), hair3 (-45° Y)
    # - Collar bones: collar0/2 (-30° Z, -90° Y), collar1 (90° X, 30° Y), collar3 (-90° X, 30° Y)
    # - Cape bones: cape0/1 (-20° Y), cape3/4 (0° X)
    # - Belt bones: belt0/1 (100° Y, ±10° X), belt2/4 (±30° Z, 120° Y), belt3/5 (90° Y, ±45° Z)
    # - Breast bones: 45° Y, ±10° X, breast_L (180° Z)
    # - Shoulder bones: 45° Y, ±70° Z, ±15° X
    def get_special_rotation(self, bone_name: str, rotation: List[float]) -> List[float]:
        """Apply special rotations based on bone name and character.
        
        Args:
            bone_name: Name of the bone
            rotation: Current rotation [x, y, z]
            
        Returns:
            Modified rotation values
        """
        # TODO: Implement special rotations from other-implementation.py
        return rotation

    def construct_keyframes(self, formatted_animation: FormattedAnimation, bones: List[BoneData]) -> List[Dict[str, Any]]:
        """Construct keyframes from animation data.
        
        Args:
            formatted_animation: Animation data from MCH format
            
        Returns:
            List of keyframes with joint transforms
        """
        keyframes: List[Dict[str, Any]] = []
        
        for frame_index, frame in enumerate(formatted_animation.frames):
            # Calculate time for this keyframe
            time = frame_index / 30.0  # 30 FPS
            
            # Process each bone pose in the frame
            joint_transforms: List[Dict[str, Any]] = []
            
            for bone_index, pose in enumerate(frame.poses):
                if isinstance(pose, RootBonePose):
                    # Root bone has location and rotation
                    rotation = [pose.x, pose.y, pose.z]
                    rotation = self.get_special_rotation("root", rotation)
                    transform = {
                        "bone_index": bone_index,
                        "location": pose.location,
                        "rotation": rotation
                    }
                else:
                    # Other bones only have rotation
                    rotation = [pose.x, pose.y, pose.z]
                    # Get bone name from skeleton
                    bone_name = bones[bone_index]["name"]
                    rotation = self.get_special_rotation(bone_name, rotation)
                    transform = {
                        "bone_index": bone_index,
                        "rotation": rotation
                    }
                
                joint_transforms.append(transform)
            
            keyframe = {
                "time": time,
                "joint_transforms": joint_transforms
            }
            keyframes.append(keyframe)
        
        return keyframes

    def __repr__(self) -> str:
        return f"ConstructedAnimation: {self.name} ({self.duration}s, {len(self.keyframes)} keyframes)" 

    def get_first_frame_pose(self) -> List[Dict[str, float]]:
        """Get the pose data from the first frame of the animation.
        
        Returns:
            List of bone rotations in radians
        """
        if not self.keyframes:
            return []
            
        first_frame = self.keyframes[0]
        rotations: List[Dict[str, float]] = []
        
        for transform in first_frame["joint_transforms"]:
            rotation = transform.get("rotation", [0.0, 0.0, 0.0])
            rotations.append({
                "rotX": rotation[0],
                "rotY": rotation[1],
                "rotZ": rotation[2]
            })
            
        return rotations 