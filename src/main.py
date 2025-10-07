import os
import bpy
import glob
import json
import hashlib
import shutil

from src.parse.headers.__parser import HeaderParser
from src.parse.model.__parser import ModelParser
from src.format.formatted_model import FormattedModel
from src.construct.__constructor import ConstructedModel
from src.export.__exporter import BlenderExporter

def calculate_gltf_hash(gltf_path: str) -> str:
    """Calculate SHA256 hash of GLTF file content
    
    Args:
        gltf_path: Path to the GLTF file
        
    Returns:
        First 8 characters of SHA256 hash
    """
    with open(gltf_path, 'rb') as f:
        content = f.read()
        hash_obj = hashlib.sha256(content)
        return hash_obj.hexdigest()[:8]

def update_gltf_index(map_name: str, model_name: str, filename: str, index_dir: str) -> None:
    """Update the GLTF index file with the new filename
    
    Args:
        map_name: Name of the map
        model_name: Name of the model
        filename: New filename with hash
        index_dir: Directory to store the index file
    """
    index_path = os.path.join(index_dir, "gltf_index.json")
    
    # Load existing index or create new one
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index = json.loads(f.read())
    else:
        index = {}
    
    # Initialize map entry if it doesn't exist
    if map_name not in index:
        index[map_name] = {}
    
    # Update model entry with filename
    index[map_name][model_name] = os.path.basename(filename)
    
    # Save updated index
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

def rename_gltf_with_hash(export_path: str, model_name: str, map_name: str) -> str:
    """Rename GLTF file and its associated files with hash. If a file with the same hash already exists,
    delete the current file instead of renaming it.
    
    Args:
        gltf_path: Path to the GLTF file
        map_name: Optional map name for logging
        
    Returns:
        New path with hash, or empty string if file was deleted
    """
    gltf_path = export_path + "/complete/" + model_name + ".gltf"
  
    if not os.path.exists(gltf_path):
        return gltf_path
        
    # Calculate hash
    hash_str = calculate_gltf_hash(gltf_path)
    
    # Get directory and filename parts
    directory = os.path.dirname(gltf_path)
    filename = os.path.basename(gltf_path)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Create new filename with hash
    new_name = f"{name_without_ext}_{hash_str}"
    new_path = os.path.join(directory, new_name + ".gltf")
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(directory), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, "gltf_export.log")
    
    # Check if file with this hash already exists
    existing_file = None
    for file in os.listdir(directory):
        if new_name in file and file.endswith('.gltf'):
            existing_file = os.path.join(directory, file)
            break
            
    if existing_file:
        # Delete current file and its associated files
        for current_file in os.listdir(directory):
            if current_file.startswith(name_without_ext + "."):
                try:
                    os.remove(os.path.join(directory, current_file))
                except OSError as e:
                    print(f"Error deleting {current_file}: {e}")
        
        # Log the skip
        with open(log_file, 'a') as f:
            map_info = f" for {map_name}" if map_name else ""
            f.write(f"Skipped matching filename{map_info}: {new_name}\n")
            
        # Update index with existing filename
        if map_name:
            update_gltf_index(map_name, name_without_ext, existing_file, export_path)
        return ""
    
    # If no existing file with same hash, rename all associated files
    for file in os.listdir(directory):
        if file.startswith(name_without_ext + "."):
            old_file = os.path.join(directory, file)
            new_file = os.path.join(directory, file.replace(name_without_ext + ".", new_name + "."))
            shutil.move(old_file, new_file)
    
    # Update bin filename reference in GLTF file
    with open(new_path, 'r') as f:
        gltf_data = json.loads(f.read())
    
    if 'buffers' in gltf_data:
        for buffer in gltf_data['buffers']:
            if 'uri' in buffer and buffer['uri'].endswith('.bin'):
                buffer['uri'] = f"{new_name}.bin"
    
    with open(new_path, 'w') as f:
        json.dump(gltf_data, f, indent=2)
    
    # Log the save
    with open(log_file, 'a') as f:
        map_info = f" for {map_name}" if map_name else ""
        f.write(f"Saved filename{map_info}: {new_name}\n")
    
    # Update index with new filename
    if map_name:
        update_gltf_index(map_name, name_without_ext, new_path, export_path)
            
    return new_path

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

        # Initialize Blender exporter
        blender_exporter = BlenderExporter()
        blender_exporter.export(constructed_model)
        print(f"Model {constructed_model.name} exported to Blender successfully")

        output_folder = os.environ.get("OUTPUT_FOLDER", "output")
        export_path_base = os.path.join(output_folder, "base")
        export_path_complete = os.path.join(output_folder, "complete")

        bpy.app.debug_value = 2
        bpy.ops.export_scene.gltf(
            filepath=export_path_complete + "/" + model_name + ".gltf",
            export_format="GLTF_SEPARATE",
            use_selection=False,
            export_apply=True,
            export_animations=True,
            export_force_sampling=True,
            export_yup=False
        )
        print(f"Model {constructed_model.name} exported to GLTF successfully at {export_path_complete}/{model_name}.gltf")

        bpy.ops.export_scene.gltf(
            filepath=export_path_base + "/" + model_name + ".gltf",
            export_format="GLTF_SEPARATE",
            use_selection=False,
            export_apply=True,
            export_animations=True,
            export_force_sampling=True,
            export_yup=False
        )
        print(f"Model {constructed_model.name} exported to base GLTF successfully at {export_path_base}/{model_name}.gltf")

        # Add hash to complete GLTF file
        rename_gltf_with_hash(output_folder, model_name, map_name)