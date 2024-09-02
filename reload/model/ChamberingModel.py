from dataclasses import dataclass

from reload.model import CaliberModel


@dataclass
class ChamberingModel:
    caliber: CaliberModel
    name: str

