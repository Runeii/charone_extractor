from typing import Optional, Tuple
from bpy.types import Object

from ..construct.constructed_mesh import ConstructedMesh
from ..construct.constructed_skeleton import ConstructedSkeleton
from ..construct.constructed_animation import ConstructedAnimation

from .blender.mesh import BlenderMeshExporter
from .blender.armature import BlenderArmatureExporter
from .blender.animation import BlenderAnimationExporter
from .blender.scene import BlenderSceneExporter

class BlenderExporter:
    """Main class for exporting constructed model data to Blender"""
    
    def __init__(self):
        self.mesh_exporter = BlenderMeshExporter()
        self.armature_exporter = BlenderArmatureExporter()
        self.animation_exporter = BlenderAnimationExporter()
        self.scene_exporter = BlenderSceneExporter()
        
    def export(self, model_data: Tuple[ConstructedMesh, ConstructedSkeleton, Optional[ConstructedAnimation]]) -> Tuple[Object, Object]:
        """
        Main export orchestration method
        
        Args:
            model_data: Tuple containing (mesh_data, skeleton_data, animation_data)
            
        Returns:
            tuple[Object, Object]: The created mesh and armature objects
        """
        mesh_data, skeleton_data, animation_data = model_data
        
        # 1. Create mesh
        mesh_obj = self.mesh_exporter.create_mesh(mesh_data)
        
        # 2. Create armature
        armature_obj = self.armature_exporter.create_armature(skeleton_data)
        
        # 3. Set up vertex groups
        self.mesh_exporter.setup_vertex_groups(mesh_obj, skeleton_data)
        
        # 4. Create animations
        if animation_data:
            self.animation_exporter.create_animation_data(animation_data)
        
        # 5. Link to scene and set up relationships
        self.scene_exporter.link_objects(mesh_obj, armature_obj)
        
        return mesh_obj, armature_obj 