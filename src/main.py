import os
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

    for _, model_header in enumerate(file_header.model_headers):
        model_name = model_header.model_name
        print(f"Processing model {model_name}")
        
        # Check if a file with model name exists in the same folder
        mch_model_file_path = os.path.join(file_directory, f"{model_name}.mch")
        if (model_name.startswith('d') == True) and (os.path.exists(mch_model_file_path) == False):
          print(f"MCH file {model_name} doesn't exist at {mch_model_file_path}, skipping")
          continue
        
        # Parse stage
        model = ModelParser(header=model_header, data=file_data, mch_model_file_path=mch_model_file_path)
        print(f"Model {model.header.model_name} parsed successfully")

        # Format stage
        formatted_model = FormattedModel(model=model)
        print(f"Model {formatted_model.name} formatted successfully")

        # Construct stage
        constructed_model = ConstructedModel(formatted_model=formatted_model)
        print(f"Model {constructed_model.name} constructed successfully")
        
        blender_exporter.export(constructed_model)
        
        print(f"Model {constructed_model.name} exported to Blender successfully")
        