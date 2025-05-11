"""Temporary bone name mappings for FF8 character models.
This module will be replaced with a different bone identification system in the future.
"""

from typing import Dict, Optional, Protocol

# Base bone names - can be extended per character type
STANDARD_BONE_NAMES: Dict[int, str] = {
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

class BoneIdentifier(Protocol):
    """Protocol for bone identification.
    This will be replaced with a more robust system in the future.
    """
    def get_bone_type(self, index: int) -> str:
        """Get the type/role of a bone by its index.
        
        Args:
            index: Bone index
            
        Returns:
            String identifying the bone's type/role
        """
        ...

class StandardBoneIdentifier:
    """Temporary bone identifier using the standard name mapping.
    This will be replaced with a more robust system in the future.
    """
    def __init__(self, character_type: Optional[str] = None):
        self.character_type = character_type
        
    def get_bone_type(self, index: int) -> str:
        """Get bone type using the standard name mapping.
        
        Args:
            index: Bone index
            
        Returns:
            Bone type/role
        """
        # ##TODO LATER: Add character-specific bone name mappings (other-implementation.py: ~400-500)
        # - Add support for hair bones (hair0-hair5)
        # - Add support for cape bones (cape0-cape5)
        # - Add support for collar bones (collar0-collar5)
        # - Add support for belt bones (belt0-belt5)
        # - Add support for dress bones (dress0-dress6)
        if self.character_type:
            pass
            
        return STANDARD_BONE_NAMES.get(index, f"bone_{index}")

# Temporary helper function for backward compatibility
def get_bone_name(index: int, character_type: Optional[str] = None) -> str:
    """Get bone name for a given index.
    This is a temporary function that will be removed in the future.
    
    Args:
        index: Bone index
        character_type: Optional character type for specific bone mappings
        
    Returns:
        Bone name
    """
    return StandardBoneIdentifier(character_type).get_bone_type(index) 