import json
from os import listdir
from os.path import isfile, join
import re
from typing import Dict, Union, List

import pyinputplus


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


  @staticmethod
  def get_files(folder_path: str, prefix: str, extension: str):
    files = [
      f for f in listdir()
      if isfile(join(folder_path, f)) and re.search(f"^{prefix}.*\.{extension}$", f)
    ]

    return files

  def select_file(self, folder_path: str, prefix: str, extension: str):
    options = self.get_files(folder_path, prefix, extension)
    if len(options) == 1:
      return options[-1]

    desired_file = pyinputplus.inputMenu(options, numbered=True)
    return join(folder_path, desired_file)
