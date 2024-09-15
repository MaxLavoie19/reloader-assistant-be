from reload.model.RecipeModel import RecipeModel
from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService


class RecipeRepository:
    def __init__(self, serializer_service: JsonSerializerService, brass_repository: BrassRepository):
        self.serializer_service = serializer_service

    def get_recipes(self, email: str):
        self.serializer_service.get_recipes(email)

    def save_recipe(self, email: str, recipe: RecipeModel):
        recipe.id
        recipe.name
        recipe.bullet_seating_depth
        recipe.min_powder_quantity_grains
        recipe.max_powder_quantity_grains
        recipe.cartridge_overall_length_mm
        recipe.cartridge_base_to_ogive_mm
        recipe.notes

        # TODO: ensure that these objects exist
        recipe.brass
        recipe.bullet
        recipe.primer
        recipe.powder