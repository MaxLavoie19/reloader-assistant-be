from dataclasses import dataclass
from typing import Union

from reload.model import ManufacturerModel


@dataclass
class PrimerModel:
    id: str
    name: str
    size: str
    manufacturer: ManufacturerModel
    barcode: Union[str, None] = None
