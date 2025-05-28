import os
import bpy
import json
import shutil

from src.parse.headers.__parser import HeaderParser
from src.parse.model.__parser import ModelParser
from src.format.formatted_model import FormattedModel
from src.construct.__constructor import ConstructedModel
from src.export.__exporter import BlenderExporter

def process_file(filepath: str) -> None:
    """Process a CharOne file and import it into Blender
    
    Args:
        filepath: Path to the .one file to process
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist")

    # Get map name from environment variable
    map_name = os.environ.get("MAP_NAME")
    if not map_name:
        raise ValueError("MAP_NAME environment variable is not set")

    with open(filepath, "rb") as f:
        file_data = f.read()

    model_headers = HeaderParser(file_data)
    print(f"Found {model_headers.model_count} models")
    
    # Get the directory of the input file
    file_directory = os.path.dirname(filepath)

    for index, model_header in enumerate(model_headers.model_headers):
        model_name = model_header.model_name
        print(f"Processing model {model_name}")

        # Check if a file with model name exists in the same folder
        model_file_path = os.path.join(file_directory, f"{model_name}.mch")
        if (model_name.startswith('d') == True) and (os.path.exists(model_file_path) == False):
          print(f"MCH file {model_name} doesn't exist at {model_file_path}, skipping")
          continue
        
        # Parse stage
        model = ModelParser(header=model_header, data=file_data)
        print(f"Model {model.header.model_name} parsed successfully")
        
        print("textures", len(model.textures))

        # Format stage
        formatted_model = FormattedModel(model=model)
        print(f"Model {formatted_model.name} formatted successfully")

        # Construct stage
        constructed_model = ConstructedModel(formatted_model=formatted_model)
        print(f"Model {constructed_model.name} constructed successfully")
        
        # Initialize Blender exporter
        blender_exporter = BlenderExporter()
        blender_exporter.export(constructed_model)
        print(f"Model {constructed_model.name} exported to Blender successfully")

        bpy.app.debug_value = 2
        bpy.ops.export_scene.gltf(
            filepath="/Users/andrew/Desktop/FF8/process/OUTPUT/bases/" + model_name + ".gltf",
            export_format="GLTF_SEPARATE",  # Export as .glb format
            use_selection=False,  # Export only selected objects (meshes/armatures)
            export_apply=True,  # Apply all transforms to the exported objects
            export_animations=True,  # Include animations in export
            export_force_sampling=True,  # Bake animations for compatibility
        )
        
        # Handle the GLTF file as JSON
        # Rename .gltf to .json
        gltf_path = "/Users/andrew/Desktop/FF8/process/OUTPUT/bases/" + model_name + ".gltf"
        json_path = "/Users/andrew/Desktop/FF8/process/OUTPUT/bases/" + model_name + ".json"
        shutil.move(gltf_path, json_path)
        
        # Read and modify JSON
        with open(json_path, 'r') as f:
            gltf_data = json.load(f)
        
        # Keep only first animation and simplify it
        if 'animations' in gltf_data and len(gltf_data['animations']) > 0:
            first_anim = gltf_data['animations'][0]
            first_anim['name'] = 'placeholder'
            if 'channels' in first_anim:
                first_anim['channels'] = [first_anim['channels'][0]]
            if 'samplers' in first_anim:
                first_anim['samplers'] = [first_anim['samplers'][0]]
            gltf_data['animations'] = [first_anim]
        else:
            gltf_data['animations'] = []
        
        # Save modified JSON
        with open(json_path, 'w') as f:
            json.dump(gltf_data, f, indent=2)
        
        # Rename back to .gltf
        shutil.move(json_path, gltf_path)
        
        bpy.ops.export_scene.gltf(
            filepath="/Users/andrew/Desktop/FF8/process/OUTPUT/animations/" + model_name + "_" + map_name + ".gltf",
            export_format="GLTF_SEPARATE",  # Export as .glb format
            use_selection=False,  # Export only selected objects (meshes/armatures)
            export_apply=True,  # Apply all transforms to the exported objects
            export_animations=True,  # Include animations in export
            export_force_sampling=True,  # Bake animations for compatibility
        )
        
        # Handle the animations GLTF file as JSON
        anim_gltf_path = "/Users/andrew/Desktop/FF8/process/OUTPUT/animations/" + model_name + "_" + map_name + ".gltf"
        anim_json_path = "/Users/andrew/Desktop/FF8/process/OUTPUT/animations/" + model_name + "_" + map_name + ".json"
        shutil.move(anim_gltf_path, anim_json_path)
        
        # Read and modify JSON
        with open(anim_json_path, 'r') as f:
            anim_data = json.load(f)
        
        # Keep only the animations key
        if 'animations' in anim_data:
            anim_data = {'animations': anim_data['animations']}
        else:
            anim_data = {'animations': []}
        
        # Save modified JSON
        with open(anim_json_path, 'w') as f:
            json.dump(anim_data, f, indent=2)
        
        # Rename back to .gltf
        shutil.move(anim_json_path, anim_gltf_path)
        