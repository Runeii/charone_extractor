from dataclasses import dataclass
from typing import List, Dict, Optional
from src.format.animations.formatted_animation import FormattedAnimation
from ..format.animations.root_bone_pose import RootBonePose
from ..format.animations.bone_pose import BonePose
import math
from mathutils import Euler, Quaternion
from .constructed_bone import ConstructedBone

@dataclass
class JointTransform:
    """Represents a single joint/bone transform in a keyframe.
    Attributes:
        bone_index: Index of the bone in the skeleton
        bone_name: Name of the bone
        location: Optional location [x, y, z] for root bone
        rotation: Rotation [x, y, z] in YXZ order
    """
    bone_index: int
    bone_name: str
    rotation: List[float]
    location: Optional[List[float]] = None

@dataclass
class Keyframe:
    """Represents a single keyframe in the animation.
    Attributes:
        frame: Frame when this occurs
        joint_transforms: List of joint transforms for this keyframe
    """
    frame_index: int
    joint_transforms: List[JointTransform]

@dataclass(init=False)
class ConstructedAnimation:
    """Constructs animation data from MCH format for Blender import.
    Attributes:
        name: Name of the animation
        frame_count: Duration of the animation in seconds
        keyframes: List of keyframes containing joint transforms
    """
    name: str
    keyframes: List[Keyframe]

    def __init__(self, formatted_animation: FormattedAnimation, bones: List[ConstructedBone], rest_pose_transforms: List[JointTransform] | None) -> None:
        """Initialize animation from formatted data."""
        self.name = formatted_animation.name
        self.frame_count = formatted_animation.frame_count

        self.keyframes = self.construct_keyframes(formatted_animation, bones, rest_pose_transforms)

    def euler_to_quaternion(self, x: float, y: float, z: float) -> Quaternion:
        """Convert XYZ Euler angles to quaternion in YXZ order"""
        rad_x = math.radians(x)
        rad_y = math.radians(y) 
        rad_z = math.radians(z)
        
        euler = Euler((rad_x, rad_y, rad_z), 'YXZ')
        return euler.to_quaternion()

    def calculate_accumulated_rotations(self, frame_poses: List[BonePose], bones: List[ConstructedBone], rest_pose_transforms: List[JointTransform] | None) -> Dict[int, Quaternion]:
        """Calculate accumulated rotations for all bones in this frame.
        
        Uses the same pattern as skeleton's combined_rotations calculation.
        """
        combined_rotations: Dict[int, Quaternion] = {}
        
        for bone_index, pose in enumerate(frame_poses):
            # Convert pose to quaternion
            if rest_pose_transforms:
              rest_quat = self.euler_to_quaternion(
                  rest_pose_transforms[bone_index].rotation[0],
                  rest_pose_transforms[bone_index].rotation[1], 
                  rest_pose_transforms[bone_index].rotation[2]
              )
              current_quat = self.euler_to_quaternion(pose.x, pose.y, pose.z)
              
              # Calculate relative rotation: rest_inverse * current
              bone_quaternion = rest_quat.conjugated() @ current_quat
            else:
                bone_quaternion = self.euler_to_quaternion(pose.x, pose.y, pose.z)
                        
            # Root bone (special case)
            if bone_index == 0:
                combined_rotations[bone_index] = bone_quaternion
            else:
                # Get parent information
                parent_id = bones[bone_index].parent
                
                # Safety check for invalid parent (same pattern as skeleton)
                if parent_id is not None and (0 > parent_id or parent_id >= len(bones)):
                    raise Exception(f"Parent bone index {parent_id} is out of range for bone {bones[bone_index].name}. Bones length: {len(bones)}")
                
                # Combine parent's rotation with this bone's rotation
                if parent_id is not None and parent_id in combined_rotations:
                    combined_rotations[bone_index] = combined_rotations[parent_id] @ bone_quaternion
                else:
                    # No valid parent - use own rotation
                    combined_rotations[bone_index] = bone_quaternion
                    
        return combined_rotations

    def construct_keyframes(self, formatted_animation: FormattedAnimation, bones: List[ConstructedBone], rest_pose_transforms: List[JointTransform] | None) -> List[Keyframe]:
        """Construct keyframes from animation data using quaternions for rotation handling."""
        keyframes: List[Keyframe] = []
        
        for frame_index, frame in enumerate(formatted_animation.frames):
            # Calculate accumulated rotations for this frame (same pattern as skeleton)
            combined_rotations = self.calculate_accumulated_rotations(frame.poses, bones, rest_pose_transforms)
            
            # Build joint transforms for this frame
            joint_transforms: List[JointTransform] = []
            
            for bone_index, pose in enumerate(frame.poses):
                if bone_index == 0:
                    local_quat = combined_rotations[bone_index]
                else:
                    parent_id = bones[bone_index].parent
                    if parent_id is not None and parent_id in combined_rotations:
                        parent_quat_inverse = combined_rotations[parent_id].conjugated()
                        local_quat = parent_quat_inverse @ combined_rotations[bone_index]
                    else:
                        local_quat = combined_rotations[bone_index]
                

                euler = local_quat.to_euler('YXZ') 
                rotation = [euler.x, euler.y, euler.z]
              
                location = None
                if bone_index == 0 and isinstance(pose, RootBonePose):
                    location = pose.location
                transform = JointTransform(
                    bone_index=bone_index,
                    bone_name=bones[bone_index].name,
                    location=location,
                   rotation=rotation
                )
                joint_transforms.append(transform)
            
            keyframe = Keyframe(frame_index=frame_index, joint_transforms=joint_transforms)
            keyframes.append(keyframe)
        
        return keyframes

    def __repr__(self) -> str:
        return f"ConstructedAnimation: {self.name}, {len(self.keyframes)} keyframes)"