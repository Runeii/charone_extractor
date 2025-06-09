from bpy.types import Object
import bpy
from src.construct.__constructor import ConstructedModel 
from math import radians

from src.export.blender.mesh import BlenderMeshExporter
from src.export.blender.armature import BlenderArmatureExporter
from src.export.blender.animation import BlenderAnimationExporter
from src.export.blender.scene import BlenderSceneExporter
from src.export.blender.rest_pose import BlenderRestPoseExporter

class BlenderExporter:
    """Main class for exporting constructed model data to Blender"""
    
    def __init__(self, reset=True):
      if reset:
        self.reset_blender()
        
      self.mesh_exporter = BlenderMeshExporter()
      self.armature_exporter = BlenderArmatureExporter()
      self.animation_exporter = BlenderAnimationExporter()
      self.scene_exporter = BlenderSceneExporter()
      self.rest_pose_exporter = BlenderRestPoseExporter()

    def reset_blender(self):
      """
      Completely reset Blender to default state
      """
      
      # Clear existing mesh from memory
      bpy.ops.object.select_all(action='SELECT')
      bpy.ops.object.delete(use_global=False)
      
      # Clear all mesh data blocks
      for mesh in bpy.data.meshes:
          bpy.data.meshes.remove(mesh)
      
      # Clear all material data blocks
      for material in bpy.data.materials:
          bpy.data.materials.remove(material)
          
      # Clear all texture data blocks
      for texture in bpy.data.textures:
          bpy.data.textures.remove(texture)
          
      # Clear all image data blocks
      for image in bpy.data.images:
          bpy.data.images.remove(image)
          
      # Clear all camera data blocks
      for camera in bpy.data.cameras:
          bpy.data.cameras.remove(camera)
          
      # Clear all light data blocks  
      for light in bpy.data.lights:
          bpy.data.lights.remove(light)
          
      # Clear all armature data blocks
      for armature in bpy.data.armatures:
          bpy.data.armatures.remove(armature)
          
      # Clear all curve data blocks
      for curve in bpy.data.curves:
          bpy.data.curves.remove(curve)
          
      # Clear all animation data
      for action in bpy.data.actions:
          bpy.data.actions.remove(action)
          
      # Clear all collections (except master collection)
      for collection in bpy.data.collections:
          bpy.data.collections.remove(collection)
          
      # Reset timeline
      scene = bpy.context.scene
      scene.frame_start = 1
      scene.frame_end = 250
      scene.frame_current = 1
      
      # Clear all keyframes from scene
      scene.animation_data_clear()
      
      # Reset world settings
      if bpy.context.scene.world:
          bpy.data.worlds.remove(bpy.context.scene.world)
      
      # Create new world
      world = bpy.data.worlds.new("World")
      bpy.context.scene.world = world
      
      
      print("Blender reset complete!")
 
    def export(self, constructed_model: ConstructedModel):
        # Check if objects with same names already exist
        mesh_name = constructed_model.name
        armature_name = constructed_model.name + "_armature"
        
        if bpy.data.objects.get(mesh_name) or bpy.data.objects.get(armature_name):
            return None, None
            
        mesh_obj = self.mesh_exporter.create_mesh(
            mesh_data=constructed_model.meshes[0],
            model_name=constructed_model.name,
            textures=constructed_model.textures
        )
        
        original_armature_obj = self.armature_exporter.create_armature(constructed_model.skeleton, constructed_model.name + "_original_armature")

        self.mesh_exporter.setup_vertex_groups(mesh_obj, constructed_model.skeleton)
        self.mesh_exporter.transform_mesh_vertices(mesh_obj, original_armature_obj, constructed_model.skeleton)
        
        self.scene_exporter.link_objects([mesh_obj, original_armature_obj])
        self.scene_exporter.setup_parent_child(original_armature_obj, mesh_obj)
        self.scene_exporter.setup_armature_modifier(mesh_obj, original_armature_obj)
        
        action = self.animation_exporter.create_animation_data(constructed_model.rest_animation)
        self.animation_exporter.setup_keyframes(original_armature_obj, constructed_model.rest_animation, action)
        
        # Setup target armature
        target_armature_obj = self.armature_exporter.create_armature(
            constructed_model.skeleton, 
            constructed_model.name + "_armature"
        )
        
        original_armature_obj.data.pose_position = 'POSE'
        original_armature_obj.animation_data.action = bpy.data.actions[mesh_name + "_action_0"]

        self.rest_pose_exporter.create_rest_pose_from_animation(mesh_obj, original_armature_obj, target_armature_obj)

        self.scene_exporter.link_objects([mesh_obj, target_armature_obj])
        self.scene_exporter.setup_parent_child(target_armature_obj, mesh_obj)
        self.scene_exporter.setup_armature_modifier(mesh_obj, target_armature_obj)

        # Clean up original armature
        for action in bpy.data.actions:
            if constructed_model.name in action.name:
              bpy.data.actions.remove(action)
        
        bpy.data.objects.remove(original_armature_obj, do_unlink=True)
    
        for animation_data in constructed_model.animations:
          action = self.animation_exporter.create_animation_data(animation_data)
          self.animation_exporter.setup_keyframes(target_armature_obj, animation_data, action)

        self.mesh_exporter.recalculate_normals(mesh_obj, target_armature_obj)
        self.setViewPreferences(target_armature_obj)

    def setViewPreferences(self, armature_obj: Object):
      armature_obj.data.pose_position    = 'POSE'

      armature_obj.data.display_type     = 'WIRE'

      for win in bpy.context.window_manager.windows:
          for area in win.screen.areas:
              if area.type == 'VIEW_3D':
                  for space in area.spaces:
                      if space.type == 'VIEW_3D':
                          space.shading.type = 'MATERIAL'
