import os
import bpy

from src.parse.headers.__parser import HeaderParser
from src.parse.model.__parser import ModelParser
from src.format.formatted_model import FormattedModel
from src.construct.__constructor import ConstructedModel
from src.export.__exporter import BlenderExporter
from src.utils.animation_hash_manager import AnimationHashManager

# All hashing functions removed as requested - no more file hashing

def process_file(filepath: str) -> None:
    """Process a CharOne file and import it into Blender
    
    Args:
        filepath: Path to the .one file to process
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist")

    with open(filepath, "rb") as f:
        file_data = f.read()

    file_header = HeaderParser(file_data)
    if file_header.model_count == 0:
      print("Didn't find any models, skipping file")
      return
    
    print(f"Found {file_header.model_count} models")

    # Initialize Blender exporter
    blender_exporter = BlenderExporter()
    
    # Get the directory of the input file
    file_directory = os.path.dirname(filepath)

    previous_tim_offset = None
    for _, model_header in enumerate(file_header.model_headers):
        model_name = model_header.model_name
        print(f"Processing model {model_name}")

        #if model_name != 'd049' and model_name != 'p017' and model_name != 'd001' and model_name != 'p001':
        #  continue
        # Check if a file with model name exists in the same folder
        mch_model_file_path = os.path.join(file_directory, f"{model_name}.mch")
        if (model_name.startswith('d') == True) and (os.path.exists(mch_model_file_path) == False):
          print(f"MCH file {model_name} doesn't exist at {mch_model_file_path}, skipping")
          continue
        
        # Parse stage
        model = ModelParser(
          header=model_header,
          data=file_data,
          mch_model_file_path=mch_model_file_path,
          previous_tim_offset=previous_tim_offset
        )

        previous_tim_offset = model.successful_tim_offset if model.successful_tim_offset is not None else previous_tim_offset
        print(f"Model {model.header.model_name} parsed successfully")
        
        print("textures", len(model.textures))

        # Format stage
        formatted_model = FormattedModel(model=model)
        print(f"Model {formatted_model.name} formatted successfully")

        # Construct stage
        constructed_model = ConstructedModel(formatted_model=formatted_model)
        print(f"Model {constructed_model.name} constructed successfully")
        # Get map name from environment variable
        map_name = os.environ.get("MAP_NAME")
        if not map_name:
          print("MAP_NAME environment variable not set, using defaul")
          blender_exporter = BlenderExporter(reset=False)
          blender_exporter.export(constructed_model)
          continue

        # CRITICAL: Start each model with a fresh scene
        print(f"Starting fresh scene for model {model_name}")
        blender_exporter = BlenderExporter()
        blender_exporter.reset_blender()
        
        # Check if the complete Blend file already exists
        output_folder = os.environ.get("OUTPUT_FOLDER", "output")
        export_path_complete = os.path.join(output_folder, "complete")
        complete_blend_path = os.path.join(export_path_complete, f"{model_name}.blend")
        file_exists = os.path.exists(complete_blend_path)
        
        print(f"Checking for existing file: {complete_blend_path}")
        print(f"File exists: {file_exists}")

        # Initialize animation hash manager
        animation_manager = AnimationHashManager(output_folder)

        if file_exists:
            print(f"File exists - merging animations with map prefix: {map_name}")
            # Load existing Blend file
            bpy.ops.wm.open_mainfile(filepath=complete_blend_path)
            
            # Find the existing armature in the loaded scene
            existing_armature_obj = None
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE' and model_name in obj.name:
                    existing_armature_obj = obj
                    break
            
            if not existing_armature_obj:
                print(f"Error: Could not find armature for model {model_name} in existing file")
                continue
                
            # Get animation hashes and update JSON tracking
            animation_hashes: List[str] = []
            for animation in constructed_model.animations:
                animation.name = "ignore"
                animation_hash = animation_manager.get_animation_hash(animation)
                animation_hashes.append(animation_hash)
                animation_manager.add_animation_to_model(map_name, model_name, animation_hash)
            
            # Use animation export with map-prefixed names
            blender_exporter.export_animations(constructed_model, existing_armature_obj, animation_hashes)
        else:
            print("File doesn't exist - creating initial export with original animation names")
            # Use full export with existing blender_exporter (scene already reset)
            blender_exporter.export(constructed_model)  # Use original animation names for initial export
            print(f"Model {constructed_model.name} exported to Blender successfully")
        # Save as Blender file to preserve all animation data perfectly
        bpy.ops.wm.save_as_mainfile(filepath=complete_blend_path)
        print(f"Model {constructed_model.name} saved to Blend file successfully at {complete_blend_path}")
        
        if file_exists:
            print(f"Overwritten existing file with merged animations")
        else:
            print(f"Created new file with initial animations")
        

        print(f"Clearing scene after initial export of model {model_name}")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Also clear any remaining data
        # Note: bpy.data collections don't have .clear() method, need to remove items individually
        for action in list(bpy.data.actions):
            bpy.data.actions.remove(action)
        for mesh in list(bpy.data.meshes):
            bpy.data.meshes.remove(mesh)
        for armature in list(bpy.data.armatures):
            bpy.data.armatures.remove(armature)
        for material in list(bpy.data.materials):
            bpy.data.materials.remove(material)
        for image in list(bpy.data.images):
            bpy.data.images.remove(image)
        for texture in list(bpy.data.textures):
            bpy.data.textures.remove(texture)
        
        print(f"Scene cleared, ready for next model")