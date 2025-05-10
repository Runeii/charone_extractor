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
        """
        Sets up armature modifier on mesh object
        
        Args:
            mesh_obj: The mesh object to add the modifier to
            armature_obj: The armature object to use as the modifier target
        """
        modifier = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
        modifier.object = armature_obj
        
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