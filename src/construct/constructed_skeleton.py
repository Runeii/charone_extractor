from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Sequence, Mapping
from src.format.formatted_bone import FormattedBone
from src.format.formatted_skin import FormattedSkin
from src.format.formatted_model import FormattedModel

from src.format.animations.formatted_animation import FormattedAnimation
from src.format.bone_names import get_bone_name
from src.format.animations.root_bone_pose import RootBonePose
from .constructed_animation import ConstructedAnimation
from .types import BoneData
import math
from mathutils import Euler, Vector

@dataclass(init=False)
class ConstructedSkeleton:
    """Constructs a skeleton from MCH format data for Blender import.
    
    Attributes:
        bones: List of bone data including name, parent, length, and transform
        rest_pose: List of bone rotations in rest pose
        skins: List of skin data for vertex-bone relationships
    """
    name: str
    bones: List[BoneData]  # List of {name, parent, length, transform, child_count, chain_length}
    rest_pose: List[Dict[str, float]]  # List of {rotX, rotY, rotZ} in radians
    formatted_bones: List[FormattedBone]
    skins: List[FormattedSkin]  # Store skin data
    
    def __init__(self, formatted_model: FormattedModel):
        self.name = formatted_model.name
        self.formatted_bones = formatted_model.bones;
        self.formatted_skins = formatted_model.skin_objects;
        self.formatted_bones = formatted_model.bones;
        self.skins = formatted_model.skin_objects;
        self.bones = self._construct_bones()
        self._calculate_bone_hierarchy()
        
        # Create a ConstructedAnimation to process the rest pose
        rest_animation = formatted_model.animations[0]
        constructed_animation = ConstructedAnimation(rest_animation, self.bones)
        self.rest_pose = constructed_animation.get_rest_pose()
        
        # Calculate bone positions from rest pose rotations
        self._calculate_bone_positions(rest_animation)

    def _calculate_bone_positions(self, rest_animation: FormattedAnimation) -> None:
        """Calculate bone positions (head/tail) and roll values from rest pose rotations."""

        for item in rest_animation.frames:
          print("is of type:", type(item).__name__)
        # Get the animation offset from the first frame of the rest animation
        root_pose: RootBonePose = rest_animation.frames[0].poses[0]
        print("first_frame", "is of type:", type(root_pose).__name__)
        offset = root_pose.location
        for i, bone in enumerate(self.formatted_bones):
            # Get rotation from rest pose
            rotation = self.rest_pose[i]
            rot_x = rotation["rotX"]
            rot_y = rotation["rotY"]
            rot_z = rotation["rotZ"]
            
            # Create Euler rotation
            eul = Euler((rot_x, rot_y, rot_z), 'YXZ')
            direction = Vector((0.0, 0.0, 1.0))
            direction.rotate(eul)
            
            if i == 0:  # Root bone
                self.bones[i]["head"] = [0.0, 0.0, 0.0]
                self.bones[i]["length"] = Vector((offset[1], offset[0], offset[2])).length
            else:
                parent_idx = self.bones[i]["parent"]
                if parent_idx is not None and 0 <= parent_idx < len(self.bones):
                    parent = self.bones[parent_idx]
                    self.bones[i]["head"] = parent["tail"]
                    self.bones[i]["length"] = bone.bone_length
            
            # Calculate tail position based on rotation and length
            scaled_length = self.bones[i]["length"] / 256.0  # Scale like the other implementation
            self.bones[i]["tail"] = [
                self.bones[i]["head"][0] + direction.x * scaled_length,
                self.bones[i]["head"][1] + direction.y * scaled_length,
                self.bones[i]["head"][2] + direction.z * scaled_length
            ]
            
            # Set roll value
            if i == 0:  # Root bone
                self.bones[i]["roll"] = math.radians(90)  # Default roll for root
            elif i == 1 or self.bones[i]["name"] in ["neck", "head"] or \
                 self.bones[i]["name"].startswith("hair") or \
                 self.bones[i]["name"].startswith("cape") or \
                 self.bones[i]["name"].startswith("collar"):
                self.bones[i]["roll"] = math.radians(-90)  # -90 degrees for these bones
            else:
                self.bones[i]["roll"] = math.radians(90)  # Default roll for other bones

        
    def _construct_bones(self) -> List[BoneData]:
        """Construct bone data from formatted bones.
        
        Args:
            formatted_bones: List of bones from MCH format
            character_type: Optional character type for bone name mapping
            
        Returns:
            List of bone data dictionaries
        """
        bones: List[BoneData] = []
        for i, bone in enumerate(self.formatted_bones):
            bone_data: BoneData = {
                "name": get_bone_name(i, self.name),
                "parent": bone.parent_bone if bone.parent_bone >= 0 else None,
                "length": bone.bone_length,
                "transform": self._calculate_bone_transform(bone),
                "child_count": 0,  # Will be calculated in _calculate_bone_hierarchy
                "chain_length": 1,  # Will be calculated in _calculate_bone_hierarchy
                "head": [0.0, 0.0, 0.0],  # Will be calculated in _calculate_rest_pose
                "tail": [0.0, 0.0, 0.0],  # Will be calculated in _calculate_rest_pose
                "roll": 0.0  # Will be calculated in _calculate_rest_pose
            }
            bones.append(bone_data)
          
        print("Bones: ", bones)
        return bones
        
    def _calculate_bone_hierarchy(self) -> None:
        """Calculate bone hierarchy information including child counts and chain lengths."""
        # Calculate child counts
        for bone in self.bones:
            if bone["parent"] is not None:
                self.bones[bone["parent"]]["child_count"] += 1
                
        # Calculate chain lengths
        for i in range(len(self.bones)):
            self.bones[i]["chain_length"] = self._calculate_chain_length(i)
            
    def _calculate_chain_length(self, bone_index: int) -> int:
        """Calculate the length of the bone chain starting from the given bone.
        
        Args:
            bone_index: Index of the bone to start from
            
        Returns:
            Length of the bone chain
        """
        length = 1
        current = bone_index
        parent = self.bones[current]["parent"]
        while parent is not None:
            length += 1
            current = parent
            parent = self.bones[current]["parent"]
        return length
        
    def _calculate_bone_transform(self, bone: FormattedBone) -> Mapping[str, Sequence[float]]:
        """Calculate bone transform matrix.
        
        Args:
            bone: Formatted bone data
            
        Returns:
            Dictionary containing transform matrix elements
        """
        # Default transform (identity matrix)
        transform = {
            "matrix": [1.0, 0.0, 0.0, 0.0,
                      0.0, 1.0, 0.0, 0.0,
                      0.0, 0.0, 1.0, 0.0,
                      0.0, 0.0, 0.0, 1.0]
        }
        return transform
        
    def get_bone_hierarchy(self) -> List[Tuple[int, Optional[int]]]:
        """Get bone parent-child relationships.
        
        Returns:
            List of (bone_index, parent_index) tuples
        """
        return [(i, bone["parent"]) for i, bone in enumerate(self.bones)]
        
    def __repr__(self) -> str:
        return f"ConstructedSkeleton: {len(self.bones)} bones, {len(self.rest_pose)} rest pose rotations" 