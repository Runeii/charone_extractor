import bpy
from bpy.types import Object

from src.construct.constructed_mesh import ConstructedMesh
from src.construct.constructed_skeleton import ConstructedSkeleton

class BlenderMeshExporter:
    """Handles creation and setup of Blender meshes"""
    
    def create_mesh(self, mesh_data: ConstructedMesh) -> Object:
        """
        Creates a Blender mesh from the constructed mesh data
        
        Args:
            mesh_data: The constructed mesh data
            
        Returns:
            Object: The created mesh object
        """
        # Create mesh and object
        mesh = bpy.data.meshes.new(name="mesh")
        obj = bpy.data.objects.new("mesh", mesh)
        
        # Create mesh from vertices and faces
        vertices = [(v["x"], v["y"], v["z"]) for v in mesh_data.vertices]
        faces = []
        for i in range(0, len(mesh_data.indices), 3):
            faces.append((mesh_data.indices[i], 
                         mesh_data.indices[i+1], 
                         mesh_data.indices[i+2]))
                
        mesh.from_pydata(vertices, [], faces)
        
        # Create UV layer
        mesh.uv_layers.new(name="UV")
        
        # Set UV coordinates for each face-vertex
        uv_layer = mesh.uv_layers[0]
        uv_idx = 0
        for face in mesh.polygons:
            for loop_idx in face.loop_indices:
                if uv_idx < len(mesh_data.uvs):
                    uv = mesh_data.uvs[uv_idx]
                    uv_layer.data[loop_idx].uv = (uv["u"], uv["v"])
                    uv_idx += 1
        
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