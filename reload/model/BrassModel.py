from dataclasses import dataclass
from typing import Union, Optional

from reload.model import ChamberingModel
from reload.model import ManufacturerModel


@dataclass
class BrassModel:
    id: str
    chambering: ChamberingModel
    manufacturer: ManufacturerModel
    barcode: Optional[str] = None
