from dataclasses import dataclass
from typing import List

@dataclass
class BulletDragModel:
  model_drag_coefficients: List[float]
  model_mach_numbers: List[float]
  drag_model_name: str
  bullet_drag_coefficients: List[float]
  diameter_mm: float
  area_mm2: float
  weight_kg: float
  weight_gn: float
