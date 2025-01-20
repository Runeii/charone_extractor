from .parse.headers.__parser import HeaderParser
from .parse.model.__parser import ModelParser

def main():
  with open("chara.one", "rb") as f:
    file_data = f.read()

  model_headers = HeaderParser(file_data)
  print(f"Found {model_headers.model_count} models")

  for model_header in model_headers:
    if model_header['is_main_field_model']:
      print(f"Skipping main field model {model_header['name']}")
      continue

    print(f"Processing model {model_header['name']}")
    model = ModelParser(header=model_header, data=file_data)
    print(f"Model {model.name} parsed successfully")    

if __name__ == "__main__":
    main()