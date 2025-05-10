import bpy
from bpy.types import Object
from mathutils import Euler

from src.construct.constructed_animation import ConstructedAnimation

class BlenderAnimationExporter:
    """Handles creation and setup of Blender animations"""
    
    def create_animation_data(self, animation_data: ConstructedAnimation) -> None:
        """
        Creates animation data blocks from the constructed animation data
        
        Args:
            animation_data: The constructed animation data
        """
        # Create action
        action = bpy.data.actions.new(name=animation_data.name)
        
        # Create F-curves for each bone
        for keyframe in animation_data.keyframes:
            for transform in keyframe["joint_transforms"]:
                bone_index = transform["bone_index"]
                
                # Create location F-curves
                if "location" in transform:
                    loc_curves = []
                    for i in range(3):
                        curve = action.fcurves.new(
                            data_path=f"pose.bones[\"{bone_index}\"].location",
                            index=i
                        )
                        loc_curves.append(curve)
                        
                    # Add location keyframes
                    for i, curve in enumerate(loc_curves):
                        curve.keyframe_points.add(1)
                        curve.keyframe_points[-1].co = (keyframe["time"], transform["location"][i])
                
                # Create rotation F-curves
                if "rotation" in transform:
                    rot_curves = []
                    for i in range(3):
                        curve = action.fcurves.new(
                            data_path=f"pose.bones[\"{bone_index}\"].rotation_euler",
                            index=i
                        )
                        rot_curves.append(curve)
                        
                    # Add rotation keyframes
                    euler = Euler(transform["rotation"], 'XYZ')
                    for i, curve in enumerate(rot_curves):
                        curve.keyframe_points.add(1)
                        curve.keyframe_points[-1].co = (keyframe["time"], euler[i])
                        
        # Set action to use fake user to prevent deletion
        action.use_fake_user = True
            
    def setup_keyframes(self, armature_obj: Object, animation_data: ConstructedAnimation) -> None:
        """
        Sets up keyframes for the armature
        
        Args:
            armature_obj: The armature object to set up keyframes for
            animation_data: The animation data containing keyframe information
        """
        # Set armature to use the action
        if not armature_obj.animation_data:
            armature_obj.animation_data_create()
            
        armature_obj.animation_data.action = bpy.data.actions[animation_data.name] 