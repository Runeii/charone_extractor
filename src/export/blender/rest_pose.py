import bpy
from bpy.types import Object
from typing import List

class BlenderRestPoseExporter:
    def create_rest_pose_from_all_meshes(self, mesh_objects: List[Object], source_armature_obj: Object, target_armature_obj: Object, frame_number: int = 1):
        # Store original frame
        original_frame = bpy.context.scene.frame_current
        
        # Capture pose transforms from SOURCE armature (the one with animation)
        pose_transforms = self.capture_pose_transforms(source_armature_obj, frame_number)
        
        # Apply current mesh deformation as rest for ALL meshes
        for mesh_obj in mesh_objects:
            self.apply_current_mesh_deformation_as_rest(mesh_obj, source_armature_obj)
        
        # Apply transforms as new rest pose to TARGET armature
        self.apply_transforms_as_rest_pose(target_armature_obj, pose_transforms)
        
        # Restore original frame
        bpy.context.scene.frame_set(original_frame)

    def capture_rest_pose_matrices(self, armature_obj: Object):
        """
        Capture rest pose matrices without scene evaluation
        """
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')
        rest_matrices = {}
        for edit_bone in armature_obj.data.edit_bones:
            rest_matrices[edit_bone.name] = {
                'matrix': edit_bone.matrix.copy()
            }
        bpy.ops.object.mode_set(mode='OBJECT')
        return rest_matrices

    def capture_pose_transforms(self, armature_obj: Object, frame_number: int = 1):
        """
        Capture pose transforms for rest pose application
        """
        bpy.context.scene.frame_set(frame_number)
        bpy.context.view_layer.update()  # Ensure scene is evaluated
        
        pose_transforms = {}
        armature_world_matrix = armature_obj.matrix_world
        
        for pose_bone in armature_obj.pose.bones:
            # Get the pose bone's world matrix relative to armature
            local_matrix = armature_world_matrix.inverted() @ pose_bone.matrix
            pose_transforms[pose_bone.name] = {
                'matrix': local_matrix.copy()
            }
        return pose_transforms

    def apply_current_mesh_deformation_as_rest(self, mesh_obj: Object, armature_obj: Object):
        """Apply the current deformed mesh state as the new rest mesh"""
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Get the evaluated (deformed) mesh
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = mesh_obj.evaluated_get(depsgraph)
        eval_mesh = eval_obj.data
        
        # Apply deformed vertex positions to the original mesh
        for i, vertex in enumerate(mesh_obj.data.vertices):
            vertex.co = eval_mesh.vertices[i].co
        
        mesh_obj.data.update()
        print(f"Applied current deformation to mesh: {mesh_obj.name}")

    def apply_transforms_as_rest_pose(self, armature_obj: Object, pose_transforms: dict):
        """Apply the captured transforms as the new rest pose"""
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        for edit_bone in armature_obj.data.edit_bones:
            if edit_bone.name in pose_transforms:
                edit_bone.matrix = pose_transforms[edit_bone.name]['matrix']
        
        bpy.ops.object.mode_set(mode='OBJECT')
        print(f"Applied new rest pose to armature: {armature_obj.name}")

    def clear_pose_transformations(self, armature_obj: Object):
        """Clear all pose bone transformations to prevent double transformation"""
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='POSE')
        
        # Clear all pose bone transformations
        for pose_bone in armature_obj.pose.bones:
            pose_bone.location = (0, 0, 0)
            pose_bone.rotation_quaternion = (1, 0, 0, 0)
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.scale = (1, 1, 1)
        
        # Update the scene
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Cleared pose bone transformations")