import json
from typing import Any

def save_to_json(dict_data: dict[str, Any], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)