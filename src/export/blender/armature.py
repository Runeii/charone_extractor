from typing import List, Dict, Any
import bpy
from bpy.types import Object
from mathutils import Vector

from src.construct.constructed_skeleton import ConstructedSkeleton

class BlenderArmatureExporter:
    """Handles creation and setup of Blender armatures"""
    
    def create_armature(self, skeleton_data: ConstructedSkeleton) -> Object:
        """
        Creates a Blender armature from the constructed skeleton data
        
        Args:
            skeleton_data: The constructed skeleton data
            
        Returns:
            Object: The created armature object
        """
        # Create armature and object
        armature = bpy.data.armatures.new(name="armature")
        obj = bpy.data.objects.new("armature", armature)
        
        # Link to scene
        bpy.context.scene.collection.objects.link(obj)
        
        # Set as active object
        bpy.context.view_layer.objects.active = obj
        
        # Enter edit mode to create bones
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Create bones
        for bone in skeleton_data.bones:
            edit_bone = armature.edit_bones.new(bone["name"])
            
            # Set bone positions
            edit_bone.head = Vector(bone["head"])
            edit_bone.tail = Vector(bone["tail"])
            
            # Set parent if exists
            if bone["parent"] is not None:
                edit_bone.parent = armature.edit_bones[skeleton_data.bones[bone["parent"]]["name"]]
                edit_bone.use_connect = True
                
            # Set roll
            edit_bone.roll = bone["roll"]
            
        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return obj
        
    def setup_bone_hierarchy(self, armature_obj: Object, bone_data: List[Dict[str, Any]]) -> None:
        """
        Sets up bone hierarchy and properties
        
        Args:
            armature_obj: The armature object to set up
            bone_data: The bone data containing hierarchy information
        """
        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Set up bone hierarchy
        for bone in bone_data:
            edit_bone = armature_obj.data.edit_bones[bone["name"]]
            
            # Set parent if exists
            if bone["parent"] is not None:
                edit_bone.parent = armature_obj.data.edit_bones[bone_data[bone["parent"]]["name"]]
                edit_bone.use_connect = True
                
            # Set roll
            edit_bone.roll = bone["roll"]
            
        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT') 