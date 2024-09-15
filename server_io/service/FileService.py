import json
from typing import Dict, Union, List


class FileService:
    @staticmethod
    def load(file_path: str) -> Union[List[Dict], Dict, None]:
        try:
            with open(file_path) as file:
                data = json.load(file)
        except FileNotFoundError:
            return None
        return data

    @staticmethod
    def save(file_path: str, data: Union[List[Dict], Dict]):
        with open(file_path, 'w') as file:
            json.dump(data, file)
