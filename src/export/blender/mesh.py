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
        
        # Set UV coordinates
        uv_layer = mesh.uv_layers[0]
        for i, uv in enumerate(mesh_data.uvs):
            uv_layer.data[i].uv = (uv["u"], uv["v"])
        
        return obj
        
    def setup_vertex_groups(self, mesh_obj: Object, skeleton_data: ConstructedSkeleton) -> None:
        """
        Sets up vertex groups for the mesh based on skeleton data
        
        Args:
            mesh_obj: The mesh object to set up vertex groups for
            skeleton_data: The skeleton data containing bone information
        """
        # Create vertex groups for each bone
        for bone in skeleton_data.bones:
            group = mesh_obj.vertex_groups.new(name=bone["name"])
            
            # Find vertices that belong to this bone
            for skin in skeleton_data.skins:
                if skin.bone_id == bone["name"]:
                    # Add vertices to group with weight 1.0
                    group.add(range(skin.first_vertex_index, 
                                  skin.first_vertex_index + skin.vertex_count), 
                            1.0, 'REPLACE') 