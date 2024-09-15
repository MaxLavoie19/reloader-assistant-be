from dataclasses import dataclass
from typing import Union

from reload.model.CaliberModel import CaliberModel
from reload.model import ManufacturerModel


@dataclass
class BulletModel:
    id: str
    caliber: CaliberModel
    manufacturer: ManufacturerModel
    model: str
    weight_in_grains: float
    g1_ballistic_coefficient: Union[float, None]
    g7_ballistic_coefficient: Union[float, None]
    sectional_density: Union[float, None]
    barcode: Union[str, None] = None
