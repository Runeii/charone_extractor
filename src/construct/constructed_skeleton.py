from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional, Sequence, Mapping, TypedDict
from math import pi
from ..format.formatted_bone import FormattedBone
from ..format.formatted_skin import FormattedSkin
import math

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
        bone_names: Mapping of bone indices to names
    """
    bones: List[BoneData]  # List of {name, parent, length, transform, child_count, chain_length}
    rest_pose: List[Dict[str, float]]  # List of {rotX, rotY, rotZ} in radians
    bone_names: Dict[int, str]  # Mapping of bone indices to names
    
    def __init__(self, formatted_bones: List[FormattedBone], 
                 formatted_skins: List[FormattedSkin],
                 rest_pose_data: Optional[bytes] = None,
                 character_type: Optional[str] = None):
        """Initialize skeleton from formatted data.
        
        Args:
            formatted_bones: List of bones from MCH format
            formatted_skins: List of skin objects for vertex mapping
            rest_pose_data: Optional animation data for rest pose
            character_type: Optional character type for bone name mapping
        """
        self.bone_names = self._get_bone_names(character_type)
        self.bones = self._construct_bones(formatted_bones)
        self._calculate_bone_hierarchy()
        self.rest_pose = self._calculate_rest_pose(rest_pose_data) if rest_pose_data else []
        
    def _get_bone_names(self, character_type: Optional[str] = None) -> Dict[int, str]:
        """Get mapping of bone indices to names.
        
        Args:
            character_type: Optional character type for specific bone mappings
            
        Returns:
            Dictionary mapping bone indices to names
        """
        # Base bone names - can be extended per character type
        names = {
            0: "root",
            1: "upperbody",
            2: "lowerbody",
            3: "neck",
            4: "head",
            5: "shoulder_L",
            6: "shoulder_R",
            7: "arm_L",
            8: "arm_R",
            9: "forearm_L",
            10: "forearm_R",
            11: "hand_L",
            12: "hand_R",
            13: "hip_L",
            14: "hip_R",
            15: "thigh_L",
            16: "thigh_R",
            17: "tibia_L",
            18: "tibia_R",
            19: "foot_L",
            20: "foot_R"
        }
        
        # ##TODO LATER: Add character-specific bone name mappings (other-implementation.py: ~400-500)
        # - Add support for hair bones (hair0-hair5)
        # - Add support for cape bones (cape0-cape5)
        # - Add support for collar bones (collar0-collar5)
        # - Add support for belt bones (belt0-belt5)
        # - Add support for dress bones (dress0-dress6)
        if character_type:
            pass
            
        return names
        
    def _construct_bones(self, formatted_bones: List[FormattedBone]) -> List[BoneData]:
        """Construct bone data from formatted bones.
        
        Args:
            formatted_bones: List of bones from MCH format
            
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
                "name": self.bone_names.get(i, f"bone_{i}"),
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
        
    def _calculate_rest_pose(self, rest_pose_data: bytes) -> List[Dict[str, float]]:
        """Calculate bone rotations for rest pose.
        
        Args:
            rest_pose_data: Animation data containing rest pose
            
        Returns:
            List of bone rotations in radians
        """
        rotations: List[Dict[str, float]] = []
        
        # Read animation header
        bone_count = int.from_bytes(rest_pose_data[2:4], byteorder='little')
        
        # Read root offset
        offset_y = int.from_bytes(rest_pose_data[4:6], byteorder='little')
        offset_x = int.from_bytes(rest_pose_data[6:8], byteorder='little')
        offset_z = int.from_bytes(rest_pose_data[8:10], byteorder='little')
        
        # Handle negative values
        if offset_y > 0x8000: offset_y -= 0x10000
        if offset_x > 0x8000: offset_x -= 0x10000
        if offset_z > 0x8000: offset_z -= 0x10000
        
        # Read bone rotations
        pose_data = rest_pose_data[10:10 + (bone_count * 4)]  # Each pose is 4 bytes
        for i in range(bone_count):
            pose_bytes = pose_data[i*4:(i+1)*4]
            
            # Decode rotation values
            byte1, byte2, byte3, byte4 = pose_bytes
            
            # Calculate raw rotations
            rot_z = ((byte1 | ((byte4 & 0x03) << 8)) << 2)
            rot_x = ((byte2 | ((byte4 & 0x0C) << 6)) << 2)
            rot_y = ((byte3 | ((byte4 & 0x30) << 4)) << 2)
            
            # Handle negative values
            if rot_x >= 0x800: rot_x -= 0x1000
            if rot_y >= 0x800: rot_y -= 0x1000
            if rot_z >= 0x800: rot_z -= 0x1000
            
            # Convert to radians
            rot_x = pi * rot_x / 0x800
            rot_y = pi * rot_y / 0x800
            rot_z = pi * rot_z / 0x800
            
            # ##TODO LATER: Add more special bone rotations (other-implementation.py: ~600-800)
            # - Add special rotations for collar bones
            # - Add special rotations for cape bones
            # - Add special rotations for belt bones
            # - Add special rotations for dress bones
            # - Add special rotations for hair bones
            if i == 1:  # upperbody
                rot_y -= pi * 85 / 180  # -85 degrees
            elif i == 2:  # lowerbody
                if rot_x > 0:
                    rot_y -= pi * 90 / 180  # -90 degrees
                else:
                    rot_y += pi * 90 / 180  # 90 degrees
            elif self.bones[i]["name"] == "neck":
                rot_y += pi  # 180 degrees
            elif self.bones[i]["name"] == "head":
                rot_y += pi * 170 / 180  # 170 degrees
            
            # Store rotation
            rotation = {
                "rotX": rot_x,
                "rotY": rot_y,
                "rotZ": rot_z
            }
            rotations.append(rotation)
            
            # Calculate bone positions
            if i == 0:  # Root bone
                self.bones[i]["head"] = [0.0, 0.0, 0.0]
                self.bones[i]["length"] = ((offset_x**2 + offset_y**2 + offset_z**2)**0.5) / 256.0
            else:
                parent_idx = self.bones[i]["parent"]
                if parent_idx is not None and 0 <= parent_idx < len(self.bones):
                    parent = self.bones[parent_idx]
                    self.bones[i]["head"] = parent["tail"]
            
            # ##TODO LATER: Add character-specific bone direction vectors (other-implementation.py: ~900-1000)
            # - Add support for different base direction vectors per character type
            # - Add character-specific position adjustments
            # Calculate tail position based on rotation and length
            # Start with base direction vector (0,0,1)
            direction = [0.0, 0.0, 1.0]
            
            # Apply rotations in YXZ order
            # First rotate around Y
            cos_y = math.cos(rot_y)
            sin_y = math.sin(rot_y)
            x = direction[0] * cos_y - direction[2] * sin_y
            z = direction[0] * sin_y + direction[2] * cos_y
            direction[0] = x
            direction[2] = z
            
            # Then rotate around X
            cos_x = math.cos(rot_x)
            sin_x = math.sin(rot_x)
            y = direction[1] * cos_x - direction[2] * sin_x
            z = direction[1] * sin_x + direction[2] * cos_x
            direction[1] = y
            direction[2] = z
            
            # Finally rotate around Z
            cos_z = math.cos(rot_z)
            sin_z = math.sin(rot_z)
            x = direction[0] * cos_z - direction[1] * sin_z
            y = direction[0] * sin_z + direction[1] * cos_z
            direction[0] = x
            direction[1] = y
            
            # Scale direction by bone length and add to head position
            scaled_length = self.bones[i]["length"] / 256.0
            self.bones[i]["tail"] = [
                self.bones[i]["head"][0] + direction[0] * scaled_length,
                self.bones[i]["head"][1] + direction[1] * scaled_length,
                self.bones[i]["head"][2] + direction[2] * scaled_length
            ]
            
            # ##TODO LATER: Add proper bone roll calculations (other-implementation.py: ~300-400)
            # - Set specific roll values for different bone types
            # - Add character-specific roll adjustments
            self.bones[i]["roll"] = 0.0
            
        return rotations
        
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