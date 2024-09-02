import json
from typing import Dict, Union


class JsonFileService:
    @staticmethod
    def load(file_path: str) -> Union[Dict[str, str], None]:
        try:
            with open(file_path) as file:
                data = json.load(file)
        except FileNotFoundError:
            return None
        return data

    @staticmethod
    def save(file_path: str, data: Dict[str, str]):
        with open(file_path, 'w') as file:
            json.dump(data, file)
