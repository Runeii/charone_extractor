from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional, Sequence, Mapping, TypedDict
from src.format.formatted_bone import FormattedBone
from src.format.formatted_skin import FormattedSkin
from src.format.animations.formatted_animation import FormattedAnimation
from src.format.bone_names import get_bone_name
from .constructed_animation import ConstructedAnimation

class BoneData(TypedDict):
    name: str
    parent: Optional[int]
    length: float
    transform: Mapping[str, Sequence[float]]
    child_count: int
    chain_length: int
    head: List[float]
    tail: List[float]
    roll: float

@dataclass(init=False)
class ConstructedSkeleton:
    """Constructs a skeleton from MCH format data for Blender import.
    
    Attributes:
        bones: List of bone data including name, parent, length, and transform
        rest_pose: List of bone rotations in rest pose
    """
    bones: List[BoneData]  # List of {name, parent, length, transform, child_count, chain_length}
    rest_pose: List[Dict[str, float]]  # List of {rotX, rotY, rotZ} in radians
    formatted_bones: List[FormattedBone]
    
    def __init__(self, formatted_bones: List[FormattedBone], 
                 formatted_skins: List[FormattedSkin],
                 rest_animation: FormattedAnimation,
                 character_type: Optional[str] = None):
        """Initialize skeleton from formatted data.
        
        Args:
            formatted_bones: List of bones from MCH format
            formatted_skins: List of skin objects for vertex mapping
            rest_animation: Animation to use for rest pose (typically index 0)
            character_type: Optional character type for bone name mapping
        """
        self.formatted_bones = formatted_bones
        self.bones = self._construct_bones(formatted_bones, character_type)
        self._calculate_bone_hierarchy()
        
        # Create a ConstructedAnimation to process the rest pose
        constructed_animation = ConstructedAnimation(rest_animation, self.bones)
        self.rest_pose = constructed_animation.get_first_frame_pose()
        
    def _get_bone_name(self, index: int, character_type: Optional[str] = None) -> str:
        """Get bone name for a given index.
        
        Args:
            index: Bone index
            character_type: Optional character type for specific bone mappings
            
        Returns:
            Bone name
        """
        return get_bone_name(index, character_type)
        
    def _construct_bones(self, formatted_bones: List[FormattedBone], character_type: Optional[str] = None) -> List[BoneData]:
        """Construct bone data from formatted bones.
        
        Args:
            formatted_bones: List of bones from MCH format
            character_type: Optional character type for bone name mapping
            
        Returns:
            List of bone data dictionaries
        """
        bones: List[BoneData] = []
        for i, bone in enumerate(formatted_bones):
            # Handle bone length (negative values)
            length = bone.bone_length
            if length > 0x8000:
                length -= 0x10000
                
            bone_data: BoneData = {
                "name": self._get_bone_name(i, character_type),
                "parent": bone.parent_bone - 1 if bone.parent_bone > 0 else None,
                "length": length / 256.0,  # Scale to match Blender units
                "transform": self._calculate_bone_transform(bone),
                "child_count": 0,  # Will be calculated in _calculate_bone_hierarchy
                "chain_length": 1,  # Will be calculated in _calculate_bone_hierarchy
                "head": [0.0, 0.0, 0.0],  # Will be calculated in _calculate_rest_pose
                "tail": [0.0, 0.0, 0.0],  # Will be calculated in _calculate_rest_pose
                "roll": 0.0  # Will be calculated in _calculate_rest_pose
            }
            bones.append(bone_data)
            
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
        
    def get_bone_transforms(self) -> List[Dict[str, Any]]:
        """Get bone transforms for Blender import.
        
        Returns:
            List of bone transform data
        """
        transforms: List[Dict[str, Any]] = []
        for bone in self.bones:
            transform = {
                "name": bone["name"],
                "parent": bone["parent"],
                "head": bone["head"],
                "tail": bone["tail"],
                "roll": bone["roll"]
            }
            transforms.append(transform)
        return transforms

    def __repr__(self) -> str:
        return f"ConstructedSkeleton: {len(self.bones)} bones, {len(self.rest_pose)} rest pose rotations" 