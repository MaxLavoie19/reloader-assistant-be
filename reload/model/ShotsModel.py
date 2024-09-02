from dataclasses import dataclass
from typing import Tuple, List

from reload.model import RifleModel
from reload.model import BatchModel
from reload.model import ShooterModel


@dataclass
class ShotModel:
    distance_yards: int
    shooter: ShooterModel
    rifle: RifleModel
    batch: BatchModel
    number: int
    coordinates: Tuple[float, float]
    velocities: List[float]
