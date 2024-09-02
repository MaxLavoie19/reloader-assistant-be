from dataclasses import dataclass
from typing import Union

from reload.model import ManufacturerModel


@dataclass
class PowderModel:
    name: str
    manufacturer: ManufacturerModel
    barcode: Union[str, None]
