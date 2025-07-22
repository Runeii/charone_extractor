import bpy
from bpy.types import Object
from typing import List
import bmesh
from mathutils import Vector

from src.construct.constructed_mesh import ConstructedMesh
from src.construct.constructed_skeleton import ConstructedSkeleton
from src.parse.model.tim import TIM
from .texture import BlenderTextureExporter
from math import radians

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
				vertices = [(-v["x"], v["y"], v["z"]) for v in mesh_data.vertices]
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

				# Apply UVs using UV indices from formatted faces
				uv_layer = bm.loops.layers.uv[0]
				for i, face in enumerate(bm.faces):
						# Get the corresponding formatted face
						formatted_face = mesh_data.formatted_faces[i]

						if len(face.loops) == 3:  # Triangle
								face.loops[0][uv_layer].uv = (mesh_data.uvs[formatted_face.vt2]["u"],
																						 mesh_data.uvs[formatted_face.vt2]["v"])
								face.loops[1][uv_layer].uv = (mesh_data.uvs[formatted_face.vt1]["u"],
																						 mesh_data.uvs[formatted_face.vt1]["v"])
								face.loops[2][uv_layer].uv = (mesh_data.uvs[formatted_face.vt3]["u"],
																						 mesh_data.uvs[formatted_face.vt3]["v"])
						elif len(face.loops) == 4:  # Quad
								face.loops[0][uv_layer].uv = (mesh_data.uvs[formatted_face.vt2]["u"],
																						 mesh_data.uvs[formatted_face.vt2]["v"])
								face.loops[1][uv_layer].uv = (mesh_data.uvs[formatted_face.vt1]["u"],
																						 mesh_data.uvs[formatted_face.vt1]["v"])
								face.loops[2][uv_layer].uv = (mesh_data.uvs[formatted_face.vt3]["u"],
																						 mesh_data.uvs[formatted_face.vt3]["v"])
								face.loops[3][uv_layer].uv = (mesh_data.uvs[formatted_face.vt4]["u"],
																						 mesh_data.uvs[formatted_face.vt4]["v"])

				# Update mesh and return to object mode
				bmesh.update_edit_mesh(mesh)
				bpy.ops.object.mode_set(mode='OBJECT')

				# Create and assign materials with textures
				if textures:
						# Create textures
						blender_images = self.texture_exporter.create_textures(textures, model_name)
						
						# Create materials
						materials = self.texture_exporter.create_materials(model_name, blender_images)
						
						# Add all materials to the mesh
						for material in materials:
								obj.data.materials.append(material)
						
						# Assign materials to faces based on texture index
						for i, face in enumerate(mesh.polygons):
								formatted_face = mesh_data.formatted_faces[i]
								face.material_index = formatted_face.texture_index
				
				# Rotate entire mesh to match the model's orientation
				obj.rotation_euler = (0, radians(-90), 0)
				bpy.context.view_layer.update()

				bpy.context.view_layer.objects.active = obj
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

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
						group = mesh_obj.vertex_groups.new(name=bone.name)

						# First set all vertices to weight 0
						all_vertices = list(range(len(mesh_obj.data.vertices)))
						group.add(all_vertices, 0.0, 'REPLACE')

						# Then set weight 1.0 for vertices that belong to this bone
						for skin in skeleton_data.skins:
								if skin.bone_id == i:  # This skin belongs to this bone
										# Get the vertex range for this skin
										start_idx = skin.first_vertex_index
										end_idx = start_idx + skin.vertex_count - 1

										# Add all vertices in this range with weight 1.0
										vertices_in_range = [v_idx for v_idx in range(start_idx, end_idx + 1)
																				if v_idx < len(mesh_obj.data.vertices)]

										if vertices_in_range:
												group.add(vertices_in_range, 1.0, 'REPLACE')

				# Limit each vertex to only belong to one vertex group
				bpy.context.view_layer.objects.active = mesh_obj
				bpy.ops.object.vertex_group_limit_total(limit=1)

		def transform_mesh_vertices(self, mesh_obj: Object, armature_obj: Object, constructed_skeleton: ConstructedSkeleton) -> None:
				# Process each vertex
				for i, vert in enumerate(mesh_obj.data.vertices):
						vert_pos = Vector(vert.co)

						for skin in constructed_skeleton.skins:
								min_idx = skin.first_vertex_index
								max_idx = min_idx + skin.vertex_count - 1

								if i >= min_idx and i <= max_idx:
										# Get the bone's rest position and rotation
										bone_name = constructed_skeleton.bones[skin.bone_id].name
										bone_head = Vector(armature_obj.data.bones[bone_name].head_local)

										vert_pos += bone_head

										# Update vertex coordinates
										vert.co = vert_pos

		def recalculate_normals(self, obj: Object, armature_obj: Object):
				print("Recalculating normals")
				# Make sure it's selected and active
				bpy.context.view_layer.objects.active = obj
				obj.select_set(True)
				
				# Enter edit mode
				bpy.ops.object.mode_set(mode='EDIT')
				
				# Select all faces
				bpy.ops.mesh.select_all(action='SELECT')
				
				# First make faces planar
				bpy.ops.mesh.face_make_planar()
				
				# Get the armature object (parent of the mesh)
				armature = armature_obj
				
				# For each vertex group (bone), check if normals need to be flipped
				for vgroup in obj.vertex_groups:
						bone = armature.data.bones.get(vgroup.name)
						if not bone:
								continue
						
						# Get bone direction
						bone_dir = (bone.tail - bone.head).normalized()
						
						# Select vertices in this group
						for v in obj.data.vertices:
								if vgroup.index in [g.group for g in v.groups]:
										v.select = True
						
						# Get average normal of selected faces
						bm = bmesh.from_edit_mesh(obj.data)
						selected_faces = [f for f in bm.faces if f.select]
						if not selected_faces:
								continue
						
						avg_normal = sum((f.normal for f in selected_faces), Vector((0,0,0))) / len(selected_faces)
						
						# If normal is pointing towards bone, flip it
						if avg_normal.dot(bone_dir) < 0:
								bpy.ops.mesh.flip_normals()
						
						bmesh.update_edit_mesh(obj.data)
				
				print("Recalculated normals")

				# Return to object mode
				bpy.ops.object.mode_set(mode='OBJECT')
				
				# Update the mesh
				obj.data.update()
    