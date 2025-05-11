import bpy
from bpy.types import Object
from mathutils import Euler

from src.construct.constructed_animation import ConstructedAnimation

class BlenderAnimationExporter:
    """Handles creation and setup of Blender animations"""
    
    def create_animation_data(self, animation_data: ConstructedAnimation) -> bpy.types.Action:
        """
        Creates animation data blocks from the constructed animation data
        
        Args:
            animation_data: The constructed animation data
            
        Returns:
            bpy.types.Action: The created action
        """
        # Check if action already exists
        if animation_data.name in bpy.data.actions:
            # Remove existing action
            bpy.data.actions.remove(bpy.data.actions[animation_data.name])
            
        # Create action
        action = bpy.data.actions.new(name=animation_data.name)
        
        # First, create all the F-curves we need
        f_curves = {}  # Dict to store F-curves by bone and type
        
        # Get unique bones from first keyframe
        if animation_data.keyframes:
            first_keyframe = animation_data.keyframes[0]
            for transform in first_keyframe["joint_transforms"]:
                bone_index = transform["bone_index"]
                
                # Create location curves if needed
                if "location" in transform:
                    if bone_index not in f_curves:
                        f_curves[bone_index] = {}
                    if "location" not in f_curves[bone_index]:
                        f_curves[bone_index]["location"] = []
                        for i in range(3):
                            curve = action.fcurves.new(
                                data_path=f"pose.bones[\"{bone_index}\"].location",
                                index=i
                            )
                            f_curves[bone_index]["location"].append(curve)
                
                # Create rotation curves if needed
                if "rotation" in transform:
                    if bone_index not in f_curves:
                        f_curves[bone_index] = {}
                    if "rotation" not in f_curves[bone_index]:
                        f_curves[bone_index]["rotation"] = []
                        for i in range(3):
                            curve = action.fcurves.new(
                                data_path=f"pose.bones[\"{bone_index}\"].rotation_euler",
                                index=i
                            )
                            f_curves[bone_index]["rotation"].append(curve)
        
        # Now add keyframes to the curves
        for keyframe in animation_data.keyframes:
            for transform in keyframe["joint_transforms"]:
                bone_index = transform["bone_index"]
                
                # Add location keyframes
                if "location" in transform and bone_index in f_curves and "location" in f_curves[bone_index]:
                    for i, curve in enumerate(f_curves[bone_index]["location"]):
                        curve.keyframe_points.add(1)
                        curve.keyframe_points[-1].co = (keyframe["time"], transform["location"][i])
                
                # Add rotation keyframes
                if "rotation" in transform and bone_index in f_curves and "rotation" in f_curves[bone_index]:
                    euler = Euler(transform["rotation"], 'XYZ')
                    for i, curve in enumerate(f_curves[bone_index]["rotation"]):
                        curve.keyframe_points.add(1)
                        curve.keyframe_points[-1].co = (keyframe["time"], euler[i])
        
        # Set action to use fake user to prevent deletion
        action.use_fake_user = True
        
        return action
            
    def setup_keyframes(self, armature_obj: Object, animation_data: ConstructedAnimation, action: bpy.types.Action) -> None:
        """
        Sets up keyframes for the armature
        
        Args:
            armature_obj: The armature object to set up keyframes for
            animation_data: The animation data containing keyframe information
            action: The action to use for the keyframes
        """
        # Set armature to use the action
        if not armature_obj.animation_data:
            armature_obj.animation_data_create()
            
        # Create a new action slot for this animation
        action_slot = armature_obj.animation_data.nla_tracks.new()
        action_slot.name = animation_data.name
        
        # Create a strip for this action
        strip = action_slot.strips.new(animation_data.name, 0, action)
        strip.action_frame_start = 0
        strip.action_frame_end = animation_data.duration * 30  # Convert seconds to frames at 30 FPS 