from dataclasses import dataclass

@dataclass
class RifleModel:
  muzzle_velocity_fps: float
  muzzle_distance_m: float
  scope_height_m: float
