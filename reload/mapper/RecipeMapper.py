import json
import zlib
from typing import Dict

from reload.mapper.BrassMapper import brass_to_dict_mapper
from reload.mapper.BulletMapper import bullet_to_dict_mapper
from reload.mapper.PowderMapper import powder_to_dict_mapper
from reload.mapper.PrimerMapper import primer_to_dict_mapper
from reload.model.BrassModel import BrassModel
from reload.model.BulletModel import BulletModel
from reload.model.CaliberModel import CaliberModel
from reload.model.ChamberingModel import ChamberingModel
from reload.model.ManufacturerModel import ManufacturerModel
from reload.model.PowderModel import PowderModel
from reload.model.PrimerModel import PrimerModel
from reload.model.RecipeModel import RecipeModel

BRASS_KEY = "brass"
BULLET_KEY = "bullet"
PRIMER_KEY = "primer"
POWDER_KEY = "powder"
CHAMBERING_KEY = "chambering"
CALIBER_KEY = "caliber"
MANUFACTURER_KEY = "manufacturer"


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


def recipe_camel_to_dataclass(recipe_dict: Dict):
    brass_dict = recipe_dict.get(BRASS_KEY)
    chambering_dict = brass_dict.get(CHAMBERING_KEY)
    brass_manufacturer_dict = brass_dict.get(MANUFACTURER_KEY)
    caliber_dict = chambering_dict.get(CALIBER_KEY)
    brass_manufacturer = ManufacturerModel(**brass_manufacturer_dict)
    caliber = CaliberModel(**caliber_dict)
    chambering = ChamberingModel(**{**chambering_dict, 'caliber': caliber})
    brass = BrassModel(**{**brass_dict, 'manufacturer': brass_manufacturer, 'chambering': chambering})

    bullet_dict = recipe_dict.get(BULLET_KEY)
    bullet_manufacturer_dict = bullet_dict.get(MANUFACTURER_KEY)
    bullet_manufacturer = ManufacturerModel(**bullet_manufacturer_dict)
    bullet = BulletModel(
        id=bullet_dict.get('id', ''),
        caliber=caliber,
        model=bullet_dict.get('model', ''),
        weight_in_grains=bullet_dict.get('weightInGrains', ''),
        g1_ballistic_coefficient=bullet_dict.get('g1BallisticCoefficient', ''),
        g7_ballistic_coefficient=bullet_dict.get('g7BallisticCoefficient', ''),
        sectional_density=bullet_dict.get('sectionalDensity', ''),
        manufacturer=bullet_manufacturer
    )

    primer_dict = recipe_dict.get(PRIMER_KEY)
    primer_manufacturer_dict = primer_dict.get(MANUFACTURER_KEY)
    primer_manufacturer = ManufacturerModel(**primer_manufacturer_dict)
    primer = PrimerModel(**{**primer_dict, 'manufacturer': primer_manufacturer})

    powder_dict = recipe_dict.get(POWDER_KEY)
    powder_manufacturer_dict = powder_dict.get(MANUFACTURER_KEY)
    powder_manufacturer = ManufacturerModel(**powder_manufacturer_dict)
    powder = PowderModel(**{**powder_dict, 'manufacturer': powder_manufacturer})

    recipe = RecipeModel(
        id=recipe_dict.get('id', ''),
        name=recipe_dict.get('name', ''),
        bullet_seating_depth=recipe_dict.get('bulletSeatingDepth', ''),
        min_powder_quantity_grains=recipe_dict.get('minPowderQuantityGrains', ''),
        max_powder_quantity_grains=recipe_dict.get('maxPowderQuantityGrains', ''),
        cartridge_overall_length_mm=recipe_dict.get('cartridgeOverallLengthMm', ''),
        cartridge_base_to_ogive_mm=recipe_dict.get('cartridgeBaseToOgiveMm', ''),
        brass=brass,
        bullet=bullet,
        primer=primer,
        powder=powder,
        notes=recipe_dict['notes']
    )
    return recipe


def recipe_to_qr_mapper(recipe: RecipeModel):
    # TODO: ? Use Id only. Good enough for double blind.
    brass: BrassModel = recipe.brass
    brass_value_list = []

    bullet: BulletModel = recipe.bullet
    bullet_value_list = []

    primer: PrimerModel = recipe.primer
    primer_value_list = []

    powder: PowderModel = recipe.powder
    powder_value_list = []

    recipe_value_list = [
        recipe.id,
        recipe.name,
        brass_value_list,
        bullet_value_list,
        primer_value_list,
        recipe.powder,
        recipe.bullet_seating_depth or '',
        recipe.min_powder_quantity_grains or 0,
        recipe.max_powder_quantity_grains or 0,
        recipe.cartridge_overall_length_mm or 0,
        recipe.cartridge_base_to_ogive_mm or 0,
        recipe.notes or '',
    ]
    recipe_string = json.dumps(recipe_value_list)
    compressed_recipe = zlib.compress(recipe_string.encode())


def qr_to_recipe_mapper(recipe_string: str):
    pass
