from dataclasses import dataclass
from typing import Union

from reload.model import BrassModel
from reload.model import BulletModel
from reload.model import PowderModel
from reload.model.PrimerModel import PrimerModel


@dataclass
class RecipeModel:
    id: str
    name: str
    brass: BrassModel
    bullet: BulletModel
    bullet_seating_depth: Union[float, None]
    primer: PrimerModel
    powder: PowderModel
    min_powder_quantity_grains: float
    max_powder_quantity_grains: float
    cartridge_overall_length_mm: float
    cartridge_base_to_ogive_mm: float
    notes: str
