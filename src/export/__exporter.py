from typing import Tuple
from bpy.types import Object
import bpy
from src.construct.__constructor import ConstructedModel

from src.export.blender.mesh import BlenderMeshExporter
from src.export.blender.armature import BlenderArmatureExporter
from src.export.blender.animation import BlenderAnimationExporter
from src.export.blender.scene import BlenderSceneExporter

class BlenderExporter:
    """Main class for exporting constructed model data to Blender"""
    
    def __init__(self):
        self.mesh_exporter = BlenderMeshExporter()
        self.armature_exporter = BlenderArmatureExporter()
        self.animation_exporter = BlenderAnimationExporter()
        self.scene_exporter = BlenderSceneExporter()
        
    def export(self, constructed_model: ConstructedModel) -> Tuple[Object, Object]:
        mesh_obj = self.mesh_exporter.create_mesh(
            mesh_data=constructed_model.meshes[0],
            model_name=constructed_model.name,
            textures=constructed_model.textures
        )

        armature_obj = self.armature_exporter.create_armature(constructed_model.skeleton, "armature")
        raw_armature_obj = self.armature_exporter.create_armature(constructed_model.skeleton, "raw_armature")

        self.mesh_exporter.setup_vertex_groups(mesh_obj, constructed_model.skeleton)
        self.mesh_exporter.transform_mesh_vertices(mesh_obj, armature_obj, constructed_model.skeleton)
        
        self.scene_exporter.link_objects([mesh_obj, armature_obj])        # Set up parent-child relationship and armature modifier
        self.scene_exporter.setup_parent_child(armature_obj, mesh_obj)
        self.scene_exporter.setup_armature_modifier(mesh_obj, armature_obj)
        
        for animation_data in constructed_model.animations:
            action = self.animation_exporter.create_animation_data(animation_data)
            self.animation_exporter.setup_keyframes(raw_armature_obj, animation_data, action)
            self.retarget_animation(armature_obj, raw_armature_obj)

        self.setViewPreferences(armature_obj)
        return mesh_obj, armature_obj 
      
    def setViewPreferences(self, armature_obj: Object):
      armature_obj.data.pose_position    = 'POSE'

      armature_obj.data.display_type     = 'WIRE'

      for win in bpy.context.window_manager.windows:
          for area in win.screen.areas:
              if area.type == 'VIEW_3D':
                  for space in area.spaces:
                      if space.type == 'VIEW_3D':
                          space.shading.type = 'MATERIAL'
                          
    def retarget_animation(self, armature_obj: Object, raw_armature_obj: Object):
