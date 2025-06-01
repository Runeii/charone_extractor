from bpy.types import Object
import bpy
from math import radians
from mathutils import Euler, Vector

class BlenderTransforms:
  def apply_orientation_fix(self, armature_obj: Object, mesh_object: Object):
    # Create empty parent
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    parent_fix = bpy.context.active_object
    
    if not parent_fix:
      raise Exception("Failed to create orientation fix")
    
    parent_fix.name = f"{armature_obj.name}_OrientationFix"
    

    # Default orientation fix
    parent_fix.rotation_euler = self.special_orientation_fixes(mesh_object)
    parent_fix.location = (0, 0, 0)
    
    # Parent armature to the fix
    armature_obj.parent = parent_fix
    
    # Parent meshes to the fix as well
    mesh_object.parent = parent_fix
    
    return parent_fix
  
  def special_orientation_fixes(self, mesh_object: Object):
    name = mesh_object.name

    is_mesh_humanoid = name.startswith('d') or name.startswith('p')
    
    ## Return default orientation if not humanoid
    if not is_mesh_humanoid:
      return Euler((radians(90), 0, radians(-90)))
    
    # If mesh is humanoid, we want to work out the orientation adjustment needed. Use the width, height, and depth of the armature object.
    # The longest axis should be rotated to stand in the Z axis.
    # The second longest axis should be rotated to stand in the Y axis.
    # The shortest axis should not need to be rotated and is in the X axis
  
    bbox_info = self.get_posed_mesh_bbox(mesh_object)
    
    # Get dimensions from bbox_info
    width_x = bbox_info['width_x']
    width_y = bbox_info['width_y']
    width_z = bbox_info['width_z']
    
    # Create list of dimensions with their corresponding axes
    dimensions = [
        (width_x, 'X'),
        (width_y, 'Y'),
        (width_z, 'Z')
    ]
    
    # Sort dimensions by size (largest to smallest)
    dimensions.sort(reverse=True)
    
    # Assign axes based on size
    height_axis = dimensions[0][1]  # Longest axis
    width_axis = dimensions[1][1]   # Second longest axis
    depth_axis = dimensions[2][1]   # Shortest axis
    
    print(f"Height axis: {height_axis}, Width axis: {width_axis}, Depth axis: {depth_axis}")
    
    euler = Euler((0,0,0))
    
    # Get standing up straight
    if height_axis == 'Y':
      euler.x = radians(90)
    elif height_axis == 'X':
      euler.y = radians(-90)
    
    # Rotate to face camera
    euler.z = radians(-90)

    return euler
  
  
  def get_posed_mesh_bbox(self, mesh_obj: Object) -> dict[str, tuple[float, float, float] | float]:
    """
    Get the bounding box of a posed/transformed mesh object in world space.
    
    Args:
        mesh_obj: Blender mesh object with applied transformations/pose
    
    Returns:
        dict: Contains bounding box info including min/max coords and dimensions
    """
    
    # Method 1: Using object.bound_box with world matrix transformation
    # This accounts for all transformations including pose/animation
    
    # Get the 8 corner vertices of the local bounding box
    bbox_corners: list[Vector] = [mesh_obj.matrix_world @ Vector(corner) for corner in mesh_obj.bound_box]
    
    # Find min/max coordinates in world space
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    min_z = min(corner.z for corner in bbox_corners)
    max_z = max(corner.z for corner in bbox_corners)
    
    # Calculate dimensions
    width_x = max_x - min_x
    width_y = max_y - min_y
    width_z = max_z - min_z
    
    return {
        'min_coords': (min_x, min_y, min_z),
        'max_coords': (max_x, max_y, max_z),
        'dimensions': (width_x, width_y, width_z),
        'width_x': width_x,
        'width_y': width_y,
        'width_z': width_z,
        'center': ((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
    }
