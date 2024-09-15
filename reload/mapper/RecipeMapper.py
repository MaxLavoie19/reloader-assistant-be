from reload.mapper.BrassMapper import brass_to_dict_mapper
from reload.mapper.BulletMapper import bullet_to_dict_mapper
from reload.mapper.PowderMapper import powder_to_dict_mapper
from reload.mapper.PrimerMapper import primer_to_dict_mapper
from reload.model.RecipeModel import RecipeModel


def recipe_to_dict_mapper(recipe: RecipeModel):
    return {
        'id': recipe.id,
        'name': recipe.name,
        'brass': brass_to_dict_mapper(recipe.brass),
        'bullet': bullet_to_dict_mapper(recipe.bullet),
        'primer': primer_to_dict_mapper(recipe.primer),
        'powder': powder_to_dict_mapper(recipe.powder),
        'bullet_seating_depth': recipe.bullet_seating_depth,
        'min_powder_quantity_grains': recipe.min_powder_quantity_grains,
        'max_powder_quantity_grains': recipe.max_powder_quantity_grains,
        'cartridge_overall_length_mm': recipe.cartridge_overall_length_mm,
        'cartridge_base_to_ogive_mm': recipe.cartridge_base_to_ogive_mm,
        'notes': recipe.notes,
    }
