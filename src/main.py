from .parse.headers.__parser import HeaderParser
from .parse.model.__parser import ModelParser
from .format.formatted_model import FormattedModel
from .construct.__constructor import ConstructedModel
from .export.exporter import Exporter

def main():
    with open("./INPUT/chara.one", "rb") as f:
        file_data = f.read()

    model_headers = HeaderParser(file_data)
    print(f"Found {model_headers.model_count} models")

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
        exporter = Exporter(name=constructed_model.name, model=constructed_model)
        exporter.export_as_gltf(f"./OUTPUT/{constructed_model.name}.gltf")
        print(f"Model {constructed_model.name} exported successfully")

if __name__ == "__main__":
    main()