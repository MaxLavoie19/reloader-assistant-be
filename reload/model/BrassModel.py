from dataclasses import dataclass
from typing import Union

from reload.model import ChamberingModel
from reload.model import ManufacturerModel


@dataclass
class BrassModel:
    chambering: ChamberingModel
    manufacturer: ManufacturerModel
    barcode: Union[str, None]
