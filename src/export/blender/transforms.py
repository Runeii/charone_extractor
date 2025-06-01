from bpy.types import Object
import bpy
from math import radians
from mathutils import Euler

class BlenderTransforms:
  def apply_orientation_fix(self, armature_obj: Object, mesh_object: Object, index: int):
    # Create empty parent
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    parent_fix = bpy.context.active_object
    
    if not parent_fix:
      raise Exception("Failed to create orientation fix")
    
    parent_fix.name = f"{armature_obj.name}_OrientationFix"
    

    # Default orientation fix
    parent_fix.rotation_euler = self.special_orientation_fixes(mesh_object)
    parent_fix.location = (0, index, 0)
    
    # Parent armature to the fix
    armature_obj.parent = parent_fix
    
    # Parent meshes to the fix as well
    mesh_object.parent = parent_fix
    
    return parent_fix
  
  def special_orientation_fixes(self, mesh_object: Object):
    name = mesh_object.name
    
    if name in [
      'd009',
      'd011',
      'd029',
      'd015',
      'd043',
      'd045',
      'd071',
      'p003',
      'p004',
      'p005',
      'p038',
      'p051'
    ]:
      return Euler((radians(-90),radians(-90),0))

    return Euler((radians(90), 0, radians(-90)))