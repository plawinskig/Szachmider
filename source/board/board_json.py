import json

def save_to_json(dict_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)