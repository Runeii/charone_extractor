from typing import Tuple, List
from bpy.types import Object

from src.construct.constructed_mesh import ConstructedMesh
from src.construct.constructed_skeleton import ConstructedSkeleton
from src.construct.constructed_animation import ConstructedAnimation

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
        
    def export(self, model_data: Tuple[ConstructedMesh, ConstructedSkeleton, List[ConstructedAnimation]]) -> Tuple[Object, Object]:
        """
        Main export orchestration method
        
        Args:
            model_data: Tuple containing (mesh_data, skeleton_data, animation_data_list)
            
        Returns:
            tuple[Object, Object]: The created mesh and armature objects
        """
        mesh_data, skeleton_data, animation_data_list = model_data
        
        # 1. Create mesh
        mesh_obj = self.mesh_exporter.create_mesh(mesh_data)
        
        # 2. Create armature
        armature_obj = self.armature_exporter.create_armature(skeleton_data)
        
        # 3. Set up vertex groups
        self.mesh_exporter.setup_vertex_groups(mesh_obj, skeleton_data)
        
        # 4. Create animations
        if animation_data_list:
            for animation_data in animation_data_list:
                action = self.animation_exporter.create_animation_data(animation_data)
                self.animation_exporter.setup_keyframes(armature_obj, animation_data, action)
        
        # 5. Link to scene and set up relationships
        self.scene_exporter.link_objects([mesh_obj, armature_obj])
        
        # 6. Set up parent-child relationship and armature modifier
        self.scene_exporter.setup_parent_child(armature_obj, mesh_obj)
        self.scene_exporter.setup_armature_modifier(mesh_obj, armature_obj)
        
        return mesh_obj, armature_obj 