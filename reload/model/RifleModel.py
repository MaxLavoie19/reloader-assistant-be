from dataclasses import dataclass

from reload.model import ChamberingModel
from reload.model import ShooterModel


@dataclass
class Rifle:
    chambering: ChamberingModel
    barrel_length_inches: float
    twist_rate: str
    owner: ShooterModel
