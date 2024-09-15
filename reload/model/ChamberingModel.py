from dataclasses import dataclass

from reload.model import CaliberModel


@dataclass
class ChamberingModel:
    id: str
    caliber: CaliberModel
    name: str

