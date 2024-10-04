from dataclasses import dataclass
from datetime import datetime


@dataclass
class RadarShotModel:
    shot_number: int
    speed_fps: float
    datetime: datetime
    weight_grain: float
    energy_joules: float
