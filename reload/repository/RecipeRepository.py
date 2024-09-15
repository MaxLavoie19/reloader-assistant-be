from reload.mapper.RecipeMapper import recipe_to_dict_mapper
from reload.model.RecipeModel import RecipeModel
from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService


class RecipeRepository:
    def __init__(self, serializer_service: JsonSerializerService):
        self.serializer_service = serializer_service

    def get_recipes(self, email: str):
        self.serializer_service.get_recipes(email)

    def save_recipe(self, email: str, recipe: RecipeModel):
        self.serializer_service.dump_recipe(email, recipe_to_dict_mapper(recipe))
