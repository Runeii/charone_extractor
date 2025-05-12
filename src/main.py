import os
from typing import Tuple, List

from src.parse.headers.__parser import HeaderParser
from src.parse.model.__parser import ModelParser
from src.format.formatted_model import FormattedModel
from src.construct.__constructor import ConstructedModel
from src.construct.constructed_mesh import ConstructedMesh
from src.construct.constructed_skeleton import ConstructedSkeleton
from src.construct.constructed_animation import ConstructedAnimation
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

    model_headers = HeaderParser(file_data)
    print(f"Found {model_headers.model_count} models")

    # Initialize Blender exporter
    blender_exporter = BlenderExporter()

    for index, model_header in enumerate(model_headers.model_headers):
        if index > 0:
            return
            
        print(f"Processing model {model_header.model_name}")
        
        # Parse stage
        model = ModelParser(header=model_header, data=file_data)
        print(f"Model {model.header.model_name} parsed successfully")

        # Format stage
        formatted_model = FormattedModel(model=model)
        print(f"Model {formatted_model.name} formatted successfully")

        # Construct stage
        constructed_model = ConstructedModel(formatted_model=formatted_model)
        print(f"Model {constructed_model.name} constructed successfully")
        
        blender_exporter.export(constructed_model)
        print(f"Model {constructed_model.name} exported to Blender successfully")