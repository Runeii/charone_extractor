import bpy
from bpy.types import Object, Action, FCurve
from mathutils import Euler
from typing import Dict, List, TypedDict

from src.construct.constructed_animation import ConstructedAnimation

class BoneCurves(TypedDict):
    location: List[FCurve]
    rotation: List[FCurve]

class BlenderAnimationExporter:
    """Handles creation and setup of Blender animations"""
    
    def create_animation_data(self, animation_data: ConstructedAnimation) -> Action:
        """
        Creates animation data blocks from the constructed animation data
        
        Args:
            animation_data: The constructed animation data
            
        Returns:
            bpy.types.Action: The created action
        """
        # Remove existing action if it exists
        if animation_data.name in bpy.data.actions:
            bpy.data.actions.remove(bpy.data.actions[animation_data.name])
            
        # Create new action
        action = bpy.data.actions.new(name=animation_data.name)
        
        if not animation_data.keyframes:
            return action

        f_curves = self._create_f_curves(action, animation_data)

        self._add_keyframes_to_curves(f_curves, animation_data)

        self._update_f_curves(f_curves)

        action.use_fake_user = True
        
        return action

    def _create_f_curves(self, action: Action, animation_data: ConstructedAnimation) -> Dict[str, BoneCurves]:
        """Creates F-curves for all bones in the animation"""
        f_curves: Dict[str, BoneCurves] = {}
        
        # Collect all unique bone names
        bone_names = {
            transform.bone_name
            for keyframe in animation_data.keyframes
            for transform in keyframe.joint_transforms
        }
        
        # Create F-curves for each bone
        for bone_name in bone_names:
            f_curves[bone_name] = {
                "location": [],
                "rotation": []
            }
            
            # Create location curves
            for i in range(3):
                curve = action.fcurves.new(
                    data_path=f"pose.bones[\"{bone_name}\"].location",
                    index=i
                )
                f_curves[bone_name]["location"].append(curve)
            
            # Create rotation curves
            for i in range(3):
                curve = action.fcurves.new(
                    data_path=f"pose.bones[\"{bone_name}\"].rotation_euler",
                    index=i
                )
                f_curves[bone_name]["rotation"].append(curve)
                
        return f_curves

    def _add_keyframes_to_curves(self, f_curves: Dict[str, BoneCurves], animation_data: ConstructedAnimation) -> None:
        """Adds keyframes to the F-curves"""
        for keyframe in animation_data.keyframes:
            frame_number = keyframe.frame_index
            
            for transform in keyframe.joint_transforms:
                bone_name = transform.bone_name

                # Add location keyframes (only for root bone)
                if transform.location and bone_name in f_curves:
                    for i, curve in enumerate(f_curves[bone_name]["location"]):
                        self._add_keyframe_point(curve, frame_number, transform.location[i])
                
                # Add rotation keyframes for all bones
                if transform.rotation and bone_name in f_curves:
                    euler = Euler(transform.rotation, 'YXZ')
                    for i, curve in enumerate(f_curves[bone_name]["rotation"]):
                        self._add_keyframe_point(curve, frame_number, euler[i])

    def _add_keyframe_point(self, curve: FCurve, frame: int, value: float) -> None:
        """Adds a single keyframe point to an F-curve"""
        curve.keyframe_points.add(1)
        point = curve.keyframe_points[-1]
        point.co = (frame, value)
        point.interpolation = 'LINEAR'
        point.handle_left_type = 'AUTO'
        point.handle_right_type = 'AUTO'

    def _update_f_curves(self, f_curves: Dict[str, BoneCurves]) -> None:
        """Updates all F-curves with proper sorting and handle types"""
        for bone_name in f_curves:
            for curve_type in f_curves[bone_name]:
                for curve in f_curves[bone_name][curve_type]:
                    # Sort keyframes by time
                    curve.keyframe_points.sort()
                    # Update handles
                    for point in curve.keyframe_points:
                        point.handle_left_type = 'AUTO'
                        point.handle_right_type = 'AUTO'
                    # Update the curve
                    curve.update()

    def setup_keyframes(self, armature_obj: Object, animation_data: ConstructedAnimation, action: Action) -> None:
        if not armature_obj.animation_data:
            armature_obj.animation_data_create()
            
        # Store the action in Blender's action data
        action.use_fake_user = True  # Keep the action in memory
        
        # Set up animation settings
        action.use_cyclic = True  # Make the animation loop

        armature_obj.animation_data.action = action
        
        if animation_data.keyframes:
            # Set frame range for this action
            action.frame_range = (0, animation_data.frame_count)
        
        action.use_frame_range = True
        
        for bone in armature_obj.pose.bones:
            bone.rotation_mode = 'YXZ'

        for fcurve in action.fcurves:
            fcurve.keyframe_points.sort()
            for point in fcurve.keyframe_points:
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'

            fcurve.update()
            
        armature_obj.animation_data.action = action