import bpy
from bpy.types import Object
from mathutils import Vector
from math import radians

from src.construct.constructed_skeleton import ConstructedSkeleton

class BlenderArmatureExporter:
    """Handles creation and setup of Blender armatures"""
    
    def create_armature(self, skeleton_data: ConstructedSkeleton, name: str) -> Object:
      # Create armature and object
      armature = bpy.data.armatures.new(name=name)
      obj = bpy.data.objects.new(name, armature)
      
      # Link to scene
      bpy.context.scene.collection.objects.link(obj)
      
      # Set as active object
      bpy.context.view_layer.objects.active = obj
      
      # Enter edit mode to create bones
      bpy.ops.object.mode_set(mode='EDIT')
      
      # Create bones
      for bone in skeleton_data.bones:
          edit_bone = armature.edit_bones.new(bone.name)
          
          # Set bone positions
          edit_bone.head = Vector(bone.head)
          edit_bone.tail = Vector(bone.tail)
          edit_bone.roll -= radians(90.0)

          # Set parent if exists
          if bone.parent is not None:
              edit_bone.parent = armature.edit_bones[skeleton_data.bones[bone.parent].name]
              edit_bone.use_connect = True

      
      # Exit edit mode
      bpy.ops.object.mode_set(mode='OBJECT')
      
      return obj