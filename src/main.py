import bpy
import os
import sys

from parse.headers.__parser import HeaderParser
from parse.model.__parser import ModelParser
from format.formatted_model import FormattedModel
from construct.__constructor import ConstructedModel
from export.__exporter import BlenderExporter

def process_file(filepath):
    """Process a CharOne file and import it into Blender"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist")

    with open(filepath, "rb") as f:
        file_data = f.read()

    model_headers = HeaderParser(file_data)
    print(f"Found {model_headers.model_count} models")

    # Initialize Blender exporter
    blender_exporter = BlenderExporter()

    for model_header in model_headers.model_headers:
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

        # Export stage
        model_data = (constructed_model.mesh, constructed_model.skeleton, constructed_model.animation)
        exported_objects = blender_exporter.export(model_data)
        print(f"Model {constructed_model.name} exported to Blender successfully")