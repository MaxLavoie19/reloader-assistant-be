from pathlib import Path
from typing import Dict, List


class UserFolderService:
  @staticmethod
  def get_user_folder(email: str):
    user_folder = f"./data/users/{email}"
    Path(user_folder).mkdir(parents=True, exist_ok=True)
    return user_folder

  def get_recipes_folder(self, email: str):
    recipes_folder = f"{self.get_user_folder(email)}/recipes"
    Path(recipes_folder).mkdir(parents=True, exist_ok=True)
    return recipes_folder

  def get_recipe_folder(self, email: str, recipe_name: str):
    recipe_folder = f"{self.get_recipes_folder(email)}/{recipe_name}"
    Path(recipe_folder).mkdir(parents=True, exist_ok=True)
    return recipe_folder

  def get_shooting_blocs_folder(self, email: str):
    blocs_folder = f"./{self.get_user_folder(email)}/blocks"
    Path(blocs_folder).mkdir(parents=True, exist_ok=True)
    return blocs_folder

  def get_shots_file(self, email: str, shot_dicts: List[Dict]):
    bloc_folder = self.get_shooting_blocs_folder(email)
    shot_file_name = f"{bloc_folder}/{shot_dicts[0]["datetime"]}"
    return shot_file_name

  def get_recipe_file(self, recipe_folder: str):
    return f"{recipe_folder}/recipe.json"

  def get_sessions_file(self):
    return "data/sessions.json"

  def get_shooting_block_file(self, email: str, date: str):
    return f"{self.get_shooting_blocs_folder(email)}/{date}.json"

  @staticmethod
  def get_public_file(component_type_name: str):
    data_file = f"./data/{component_type_name}.json"
    Path(data_file).mkdir(parents=True, exist_ok=True)
    return data_file

  def get_user_file(self, email: str):
    user_folder = self.get_user_folder(email)
    return f"{user_folder}/user.json"