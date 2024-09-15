import dataclasses
from pathlib import Path
from typing import Union, Dict, List

from reload.model.RecipeModel import RecipeModel
from server_io.service.FileService import FileService
from session.model.UserModel import UserModel


class JsonSerializerService:
    def __init__(self, json_file_service: FileService):
        self.json_file_service = json_file_service

    @staticmethod
    def get_user_folder(email: str):
        return f"./data/users/{email}"

    def get_recipes_folder(self, email: str):
        return f"{self.get_user_folder(email)}/recipes"

    def get_recipe_folder(self, email: str, recipe_name: str):
        return f"{self.get_recipes_folder(email)}/{recipe_name}"

    def get_shooting_blocs_folder(self, email: str):
        return f"./{self.get_user_folder(email)}/blocks"

    def get_recipe_file(self, recipe_folder: str):
        return f"{recipe_folder}/recipe.json"

    def get_sessions_file(self):
        return "data/sessions.json"

    def get_shooting_block_file(self, email: str, date: str):
        return f"{self.get_shooting_blocs_folder(email)}/{date}.json"

    @staticmethod
    def get_public_file(component_type_name: str):
        return f"./data/{component_type_name}.json"

    def get_recipes(self, email: str):
        recipes_folder = self.get_recipes_folder(email)
        recipe_folders = Path(recipes_folder).iterdir()
        recipes = []
        for recipe_folder in recipe_folders:
            recipe_file = self.get_recipe_file(recipe_folder.name)
            recipe_dict = self.json_file_service.load(recipe_file)
            recipe = RecipeModel(**recipe_dict)
            recipes.append(recipe)
        return recipes

    def get_user_file(self, email: str):
        user_folder = self.get_user_folder(email)
        Path(user_folder).mkdir(parents=True, exist_ok=True)
        return f"{user_folder}/user.json"

    def load_public_file(self, component_type_name: str) -> List[Dict]:
        file = self.get_public_file(component_type_name)
        components = self.json_file_service.load(file)
        if components is None:
            return []
        return components

    def dump_public_file(self, component_type_name: str, components: List[Dict]):
        file = self.get_public_file(component_type_name)
        self.json_file_service.save(file, components)

    def load_user(self, email: str) -> Union[Dict, None]:
        file_path = self.get_user_file(email)
        user_dict = self.json_file_service.load(file_path)
        if user_dict is None or len(user_dict) == 0:
            return None
        return user_dict

    def dump_user(self, user: UserModel):
        file_path = self.get_user_file(user.email)
        user_dict = dataclasses.asdict(user)
        self.json_file_service.save(file_path, user_dict)
