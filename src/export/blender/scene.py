from typing import List
import bpy
from bpy.types import Object

from src.export.blender.types import ( BlenderObject, Modifier as BlenderModifier )

class BlenderSceneExporter:
    """Handles scene integration and object linking"""
    
    def link_objects(self, objects: List[Object]) -> None:
        """
        Links objects to the scene
        
        Args:
            objects: List of objects to link to the scene
        """
        for obj in objects:
          if obj.name not in bpy.context.scene.collection.objects:
              bpy.context.scene.collection.objects.link(obj)
            
    def setup_parent_child(self, parent: Object, child: Object) -> None:
        """
        Sets up parent-child relationship between objects
        
        Args:
            parent: The parent object
            child: The child object
        """
        child.parent = parent
        
    def setup_armature_modifier(self, mesh_obj: Object, armature_obj: Object) -> None:
        """Set up the armature modifier on the mesh object"""
        # Give mesh object an armature modifier, using vertex groups but not envelopes
        modifier = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
        modifier.object = armature_obj
        modifier.use_bone_envelopes = False
        modifier.use_vertex_groups = True
        
    def setup_modifiers(self, mesh_obj: BlenderObject, armature_obj: BlenderObject) -> None:
        """
        Sets up armature modifier on mesh
        
        Args:
            mesh_obj: The mesh object to set up modifiers for
            armature_obj: The armature object to use for the modifier
        """
        # Add armature modifier
        modifier = BlenderModifier(mesh_obj.modifiers.new(name="Armature", type='ARMATURE'))
        modifier.object = armature_obj
        modifier.use_vertex_groups = True
        modifier.use_bone_envelopes = False 