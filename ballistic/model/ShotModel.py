from dataclasses import dataclass, field

from ballistic.model.BulletDragModel import BulletDragModel
from ballistic.model.RifleModel import RifleModel
from ballistic.model.TrajectoryModel import TrajectoryModel
from ballistic.model.WeatherConditionModel import WeatherConditionModel

@dataclass
class ShotModel:
  weather_condition: WeatherConditionModel
  bullet_drag: BulletDragModel
  rifle: RifleModel
  direction_degree: float
  velocity_m_per_s: float
  velocity_fps: float
  vertical_velocity_m_per_s: float
  horizontal_velocity_m_per_s: float
  trajectory: TrajectoryModel = field(default_factory=TrajectoryModel)
