from .parse.headers.__parser import HeaderParser
from .parse.model.__parser import ModelParser

def main():
  with open("./INPUT/chara.one", "rb") as f:
    file_data = f.read()

  model_headers = HeaderParser(file_data)
  print(f"Found {model_headers.model_count} models")

  for model_header in model_headers.model_headers:
    print(f"Processing model {model_header.model_name}")
    model = ModelParser(header=model_header, data=file_data)
    print(f"Model {model.header.model_name} parsed successfully")    

if __name__ == "__main__":
    main()