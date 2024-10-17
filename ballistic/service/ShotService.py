import math

from ballistic.model.ShotModel import ShotModel
from ballistic.model.BulletDragModel import BulletDragModel
from ballistic.model.RifleModel import RifleModel
from ballistic.model.WeatherConditionModel import WeatherConditionModel
from ballistic.service.DragCalculatorService import DragCalculatorService


GRAVITY_M_S2 = 9.807

class ShotService:
  def __init__(self, drag_calculator_service: DragCalculatorService):
    self.drag_calculator_service = drag_calculator_service

  def shoot_to_distance(
    self,
    shot: ShotModel,
    distance_m: float,
    frame_per_seconds: float
  ) -> float:
    current_distance_m = shot.trajectory.xm_positions[-1]

    while current_distance_m < distance_m + 1:
      self.update_drop(shot, frame_per_seconds)
      velocity_fps = self.drag_calculator_service.apply_drag(
        shot, shot.velocity_fps, frame_per_seconds
      )
      self.update_horizontal_and_vertical_velocity(shot, velocity_fps)
      self.update_position(shot, frame_per_seconds)
      current_distance_m = shot.trajectory.xm_positions[-1]
    return shot

  def shot_factory(
    self,
    direction_degree: float,
    weather_condition: WeatherConditionModel,
    bullet_drag: BulletDragModel,
    rifle: RifleModel,
  ) -> ShotModel:
    muzzle_velocity_m_per_s = self.fps_to_m_per_s(rifle.muzzle_velocity_fps)
    direction_radian = math.radians(direction_degree)
    vertical_velocity_m_per_s = math.sin(direction_radian) * muzzle_velocity_m_per_s
    horizontal_velocity_m_per_s = math.cos(direction_radian) * muzzle_velocity_m_per_s

    vertical_muzzle_offset_m = math.sin(direction_radian) * rifle.muzzle_distance_m
    horizontal_muzzle_offset_m = math.cos(direction_radian) * rifle.muzzle_distance_m

    shot_model = ShotModel(
      weather_condition=weather_condition,
      bullet_drag=bullet_drag,
      rifle=rifle,
      direction_degree=direction_degree,
      velocity_m_per_s=muzzle_velocity_m_per_s,
      velocity_fps=rifle.muzzle_velocity_fps,
      vertical_velocity_m_per_s=vertical_velocity_m_per_s,
      horizontal_velocity_m_per_s=horizontal_velocity_m_per_s,
    )
    trajectory = shot_model.trajectory
    trajectory.ts_positions.append(0)
    trajectory.xm_positions.append(horizontal_muzzle_offset_m)
    trajectory.ym_positions.append(vertical_muzzle_offset_m - rifle.scope_height_m)
    trajectory.v_m_per_s_positions.append(muzzle_velocity_m_per_s)
    return shot_model

  def fps_to_m_per_s(self, velocity_fps: float):
    velocity_m_per_s = velocity_fps / 3.281
    return velocity_m_per_s

  def m_per_s_to_fps(self, velocity_m_per_s: float):
    velocity_fps = velocity_m_per_s * 3.281
    return velocity_fps

  def update_horizontal_and_vertical_velocity(self, shot_model: ShotModel, velocity_fps: float):
    direction_radian = math.radians(shot_model.direction_degree)
    velocity_m_per_s = self.fps_to_m_per_s(velocity_fps)
    shot_model.velocity_fps = velocity_fps
    shot_model.velocity_m_per_s = velocity_m_per_s
    shot_model.vertical_velocity_m_per_s = math.sin(direction_radian) * velocity_m_per_s
    shot_model.horizontal_velocity_m_per_s = math.cos(direction_radian) * velocity_m_per_s

  def update_drop(self, shot_model: ShotModel, frame_per_seconds: float):
    vertical_acceleration = GRAVITY_M_S2 / frame_per_seconds
    shot_model.vertical_velocity_m_per_s -= vertical_acceleration
    shot_model.velocity_m_per_s = math.sqrt(
      math.pow(shot_model.vertical_velocity_m_per_s, 2) + \
      math.pow(shot_model.horizontal_velocity_m_per_s, 2)
    )
    shot_model.velocity_fps = self.m_per_s_to_fps(shot_model.velocity_m_per_s)
    direction_radian = math.asin(
      shot_model.vertical_velocity_m_per_s / shot_model.velocity_m_per_s
    )
    shot_model.direction_degree = math.degrees(direction_radian)

  def update_position(self, shot_model: ShotModel, frame_per_seconds: float):
    trajectory = shot_model.trajectory
    trajectory.ts_positions.append(trajectory.ts_positions[-1] + frame_per_seconds)
    trajectory.xm_positions.append(
      trajectory.xm_positions[-1] + shot_model.horizontal_velocity_m_per_s / frame_per_seconds
    )
    trajectory.ym_positions.append(
      trajectory.ym_positions[-1] + shot_model.vertical_velocity_m_per_s / frame_per_seconds
    )
    trajectory.v_m_per_s_positions.append(shot_model.velocity_m_per_s)
