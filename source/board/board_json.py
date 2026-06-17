import json
from typing import Any

def save_to_json(dict_data: dict[str, Any], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)

def load_from_json(file_path: str) -> dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)