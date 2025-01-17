from .header_parser import HeaderParser
from .parse.parsed_model import ParsedModel
from .sanitise.sanitised_model import SanitisedModel
from .export.exporter import Exporter

def main():
  with open("chara.one", "rb") as f:
    file_data = f.read()
  
  parser = HeaderParser()
  headers = parser.parse_headers(file_data)
  
  for model in headers:
    if model['is_main_field_model']:
      #print(f"Skipping main field model {model['name']}")
      continue

    print(f"Processing model {model['name']}")
    model = ParsedModel(name=model['name'], id=model['id'], model_offset=model['model_offset'], tim_offsets=model['tim_offsets'], data_offset=model['data_offset'], data=file_data)
    sanitised_model = SanitisedModel(model=model);

    #exporter = Exporter(name=model.name, model=sanitised_model)
    #exporter.export_as_obj('./output.obj')

if __name__ == "__main__":
    main()