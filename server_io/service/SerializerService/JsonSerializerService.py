import dataclasses
import sys
from pathlib import Path
from typing import Union, Dict, List

from reload.model.RecipeModel import RecipeModel
from server_io.service.UserFolderService.UserFolderService import UserFolderService
from server_io.service.FileService import FileService
from session.model.UserModel import UserModel

SESSIONS_FILE_PATH = "./data/sessions.json"


class JsonSerializerService:
  def __init__(self, json_file_service: FileService, user_folder_service: UserFolderService):
    self.json_file_service = json_file_service
    self.user_folder_service = user_folder_service

  def get_recipes(self, email: str):
    recipes_folder = self.user_folder_service.get_recipes_folder(email)
    Path(recipes_folder).mkdir(parents=True, exist_ok=True)
    recipe_folders = Path(recipes_folder).iterdir()
    recipes = []
    for recipe_folder in recipe_folders:
        recipe_file = self.user_folder_service.get_recipe_file(f"{recipe_folder}")
        print(recipe_file, file=sys.stderr)
        recipe_dict = self.json_file_service.load(recipe_file)
        recipe = RecipeModel(**recipe_dict)
        recipes.append(recipe)
    return recipes

  def dump_recipe(self, email: str, recipe_dict: Dict):
    recipe_folder = self.user_folder_service.get_recipe_folder(email, recipe_dict['name'])
    recipe_file = self.user_folder_service.get_recipe_file(recipe_folder)
    self.json_file_service.save(recipe_file, recipe_dict)

  def load_sessions(self) -> Dict[str, Dict]:
    return self.json_file_service.load(SESSIONS_FILE_PATH)

  def dump_sessions(self, sessions: Dict[str, Dict]):
    self.json_file_service.save(SESSIONS_FILE_PATH, sessions)

  def load_public_file(self, component_type_name: str) -> List[Dict]:
    file = self.user_folder_service.get_public_file(component_type_name)
    components = self.json_file_service.load(file)
    if components is None:
        return []
    return components

  def dump_public_file(self, component_type_name: str, components: List[Dict]):
    file = self.user_folder_service.get_public_file(component_type_name)
    self.json_file_service.save(file, components)

  def load_user(self, email: str) -> Union[Dict, None]:
    file_path = self.user_folder_service.get_user_file(email)
    user_dict = self.json_file_service.load(file_path)
    if user_dict is None or len(user_dict) == 0:
        return None
    return user_dict

  def dump_user(self, user: UserModel):
    file_path = self.user_folder_service.get_user_file(user.email)
    user_dict = dataclasses.asdict(user)
    self.json_file_service.save(file_path, user_dict)

  def dump_radar_readings(self, file_path: str, shot_dicts: List[Dict]):
    self.json_file_service.save(file_path, shot_dicts)
