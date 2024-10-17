import math

from typing import List
from ballistic.data.DragModels import DragModels
from ballistic.model.ShotModel import ShotModel
from ballistic.model.BulletDragModel import BulletDragModel
from ballistic.model.WeatherConditionModel import WeatherConditionModel

DRAG_MODEL_FILE_NAMES = {
   DragModels.G1: "mcg1.txt",
   DragModels.G7: "mcg7.txt",
}


class DragCalculatorService:
  def bullet_drag_model_factory(
    self,
    drag_model_name: DragModels,
    ballistic_coefficient: float,
    diameter_mm: float,
    weight_gn: float
  ):
    mach_numbers, drag_coefficients = self.load_drag_model(
       DRAG_MODEL_FILE_NAMES[drag_model_name]
    )
    projectile_drag_coefficients = self.projectile_drag_coefficients(
      ballistic_coefficient, drag_coefficients
    )

    area_mm2 = self.area_mm2(diameter_mm)
    weight_kg = self.weight_kg(weight_gn)

    bullet_drag_model = BulletDragModel(
      model_drag_coefficients=drag_coefficients,
      model_mach_numbers=mach_numbers,
      drag_model_name=drag_model_name.value,
      bullet_drag_coefficients=projectile_drag_coefficients,
      diameter_mm=diameter_mm,
      area_mm2=area_mm2,
      weight_gn=weight_gn,
      weight_kg=weight_kg,
    )
    return bullet_drag_model

  def weight_kg(self, weight_gn: float):
     weight_kg = weight_gn / 15432
     return weight_kg

  def area_mm2(self, diameter_mm: float):
     area_mm2 = math.pow(diameter_mm / 2, 2) * math.pi
     return area_mm2

  def load_drag_model(self, filename):
    with open("ballistic/data/drag_model/" + filename) as file:
        drag_model_content = file.read()

    lines = drag_model_content.split("\n")
    mach_numbers = []
    drag_coefficients = []
    for line in lines:
        if line.__len__() == 0:
            continue
        mach_number, drag_coefficient = line.split("\t")
        mach_number = float(mach_number)
        drag_coefficient = float(drag_coefficient)
        mach_numbers.append(mach_number)
        drag_coefficients.append(drag_coefficient)
    return mach_numbers, drag_coefficients

  def projectile_drag_coefficients(
      self, ballistic_coefficient: float, drag_coefficients: List[float]
    ):
    projectile_drag_coefficients = list(map(lambda x: x / ballistic_coefficient, drag_coefficients))
    return projectile_drag_coefficients

  def get_drag_coefficient(
    self,
    shot: ShotModel
  ):
    velocity_m_per_s = self.fps_to_m_per_s(shot.velocity_fps)
    mach_number = self.mach_number(shot.weather_condition, velocity_m_per_s)
    drag = 0
    previous_mach_number = 0
    previous_drag_coefficient = 0
    for next_mach_number, next_drag_coefficient in zip(
      shot.bullet_drag.model_mach_numbers, shot.bullet_drag.bullet_drag_coefficients
    ):
      if next_mach_number > mach_number:
        drag = self.linear_interpolation(
          previous_mach_number,
          previous_drag_coefficient,
          next_mach_number,
          next_drag_coefficient,
          mach_number,
        )
        break
      previous_mach_number = next_mach_number
      previous_drag_coefficient = next_drag_coefficient
    return drag

  def get_drag(
    self,
    shot: ShotModel
  ):
    drag_coefficient = self.get_drag_coefficient(shot)
    velocity_m_per_s = self.fps_to_m_per_s(shot.velocity_fps)
    area_m2 = self.mm2_to_m2(shot.bullet_drag.area_mm2)
    drag_force = self.drag_force(
      shot.weather_condition.air_density, velocity_m_per_s, drag_coefficient, area_m2
    )
    return drag_force

  def apply_drag(
    self,
    shot: ShotModel,
    velocity_fps: float,
    frame_per_seconds: float
  ):
    drag = self.get_drag(shot)
    acceleration = -drag / shot.bullet_drag.weight_kg
    return velocity_fps + acceleration / frame_per_seconds

  def mm2_to_m2(self, area_mm2):
     return area_mm2 / 1e6

  def fps_to_m_per_s(self, velocity_fps: float):
    velocity_m_per_s = velocity_fps / 3.281
    return velocity_m_per_s

  def mach_number(
    self, weather_condition: WeatherConditionModel, velocity_m_per_s: float
  ):
    mach_number = velocity_m_per_s / weather_condition.speed_of_sound_m_per_s
    return mach_number

  def drag_force(
    self, fluid_mass_density_kg_per_m3, flow_velocity_meter_per_seconds, drag_coefficient, area_m2
  ):
    """
      https://en.wikipedia.org/wiki/Drag_equation
      Fd = p u^2 Cd A / 2
      Fd is the drag force
      p is the mass density of the fluid
      u is the flow velocity relative to the object
      Cd is the drag coefficient
      A is the reference area
    """
    velocity_squared = pow(flow_velocity_meter_per_seconds, 2)
    drag_force = fluid_mass_density_kg_per_m3 * velocity_squared * drag_coefficient * area_m2 / 2
    return drag_force

  def linear_interpolation(self, x1: float, y1: float, x2: float, y2: float, x: float):
      diff_x = x2 - x1
      diff_y = y2 - y1
      desired_x_diff = x - x1
      x_ratio = desired_x_diff / diff_x
      y = y1 + (diff_y * x_ratio)
      return y
