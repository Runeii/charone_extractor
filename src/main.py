from .header import CharacterFileParser
from .model import Model

def main():
    with open("chara.one", "rb") as f:
        file_data = f.read()
    
    parser = CharacterFileParser(debug=True)
    headers = parser.parse_headers(file_data)
    
    print(f"\nFound {len(headers)} models:")
    for model in headers:
        if model['tim_offsets'] == []:
            continue
        model = Model(name=model['name'], id=model['id'], model_offset=model['model_offset'], tim_offsets=model['tim_offsets'], data_offset=model['data_offset'], data=file_data)
        print(model)

if __name__ == "__main__":
    main()