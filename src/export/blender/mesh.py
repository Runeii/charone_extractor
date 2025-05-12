import bpy
from bpy.types import Object
from typing import List
import bmesh

from src.construct.constructed_mesh import ConstructedMesh
from src.construct.constructed_skeleton import ConstructedSkeleton
from src.parse.model.tim import TIM
from .texture import BlenderTextureExporter

class BlenderMeshExporter:
    """Handles creation and setup of Blender meshes"""
    
    def __init__(self):
        self.texture_exporter = BlenderTextureExporter()
    
    def create_mesh(self, mesh_data: ConstructedMesh, model_name: str, textures: List[TIM]) -> Object:
        """
        Creates a Blender mesh from the constructed mesh data
        
        Args:
            mesh_data: The constructed mesh data
            model_name: Name of the model
            textures: List of TIM textures
            
        Returns:
            Object: The created mesh object
        """
        # Create mesh and object
        mesh = bpy.data.meshes.new(name=f"{model_name}_mesh")
        obj = bpy.data.objects.new(model_name, mesh)
        
        # Link object to scene collection
        bpy.context.scene.collection.objects.link(obj)
        
        # Create mesh from vertices and faces
        vertices = [(v["x"], v["y"], v["z"]) for v in mesh_data.vertices]
        faces = mesh_data.faces
                
        mesh.from_pydata(vertices, [], faces)
        
        # Create UV layer with model-specific name
        mesh.uv_layers.new(name=f"{model_name}UV")
        
        # Switch to edit mode and get bmesh
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(mesh)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        
        
        # Apply UVs using face vertex indices
        uv_layer = bm.loops.layers.uv[0]
        for i, face in enumerate(bm.faces):
            if len(face.loops) == 3:  # Triangle
                face.loops[0][uv_layer].uv = (mesh_data.uvs[face.verts[0].index]["u"], 
                                             mesh_data.uvs[face.verts[0].index]["v"])
                face.loops[1][uv_layer].uv = (mesh_data.uvs[face.verts[1].index]["u"], 
                                             mesh_data.uvs[face.verts[1].index]["v"])
                face.loops[2][uv_layer].uv = (mesh_data.uvs[face.verts[2].index]["u"], 
                                             mesh_data.uvs[face.verts[2].index]["v"])
            elif len(face.loops) == 4:  # Quad
                face.loops[0][uv_layer].uv = (mesh_data.uvs[face.verts[0].index]["u"], 
                                             mesh_data.uvs[face.verts[0].index]["v"])
                face.loops[1][uv_layer].uv = (mesh_data.uvs[face.verts[1].index]["u"], 
                                             mesh_data.uvs[face.verts[1].index]["v"])
                face.loops[2][uv_layer].uv = (mesh_data.uvs[face.verts[2].index]["u"], 
                                             mesh_data.uvs[face.verts[2].index]["v"])
                face.loops[3][uv_layer].uv = (mesh_data.uvs[face.verts[3].index]["u"], 
                                             mesh_data.uvs[face.verts[3].index]["v"])
        
        # Update mesh and return to object mode
        bmesh.update_edit_mesh(mesh)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create and assign material with textures
        if textures:
            # Create textures
            blender_images = self.texture_exporter.create_textures(textures, model_name)
            
            # Create material
            material = self.texture_exporter.create_material(model_name, blender_images)
            
            # Assign material to mesh
            obj.data.materials.append(material)
        
        return obj
        
    def setup_vertex_groups(self, mesh_obj: Object, skeleton_data: ConstructedSkeleton) -> None:
        """
        Sets up vertex groups for the mesh based on skeleton data
        
        Args:
            mesh_obj: The mesh object to set up vertex groups for
            skeleton_data: The skeleton data containing bone information
        """
        # Create vertex groups for each bone
        for i, bone in enumerate(skeleton_data.bones):
            group = mesh_obj.vertex_groups.new(name=bone["name"])
            
            # First set all vertices to weight 0
            all_vertices = list(range(len(mesh_obj.data.vertices)))
            for vertex_idx in all_vertices:
                group.add([vertex_idx], 0.0, 'REPLACE')
            
            # Then set weight 1.0 for vertices that belong to this bone
            # Since vertices are already reordered by skin groups, we can use the indices directly
            for skin in skeleton_data.skins:
                if skin.bone_id == i:  # Compare with bone index instead of name
                    for j in range(skin.vertex_count):
                        vertex_idx = skin.first_vertex_index + j
                        if vertex_idx < len(mesh_obj.data.vertices):
                            group.add([vertex_idx], 1.0, 'REPLACE') 