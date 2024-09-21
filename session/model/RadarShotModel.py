import datetime as datetime
from dataclasses import dataclass


@dataclass
class RadarShotModel:
    shot_number: int
    speed_fps: float
    datetime: datetime
    weight_grain: float
    energy_joules: float
