import math
import matplotlib.pyplot as plt
import numpy as np

from ballistic.model.RifleModel import RifleModel
from ballistic.model.ShotModel import ShotModel
from ballistic.service.InterpolationService import InterpolationService
from ballistic.service.WeatherConditionService import WeatherConditionService
from ballistic.service.DragCalculatorService import DragCalculatorService
from ballistic.service.ShotService import ShotService
from ballistic.data.DragModels import DragModels

BERGER_6_5_140_GN_HYBRID_TARGET_G7 = 0.311
HORNADY_6_5_140_BTHP_G7 = 0.288
BULLET_G7_BC = BERGER_6_5_140_GN_HYBRID_TARGET_G7

YARDS_100_IN_M = 91.44
ZERO_DISTANCE = YARDS_100_IN_M
MUZZLE_VELOCITY_FPS = 2316
FRAME_PER_SECONDS = 10000.0
SCOPE_HEIGHT_M = 43.5 / 1000
MUZZLE_DISTANCE_M = .8

TEMPERATURE_C = 27
ATMOSPHERIC_PRESSURE_KPA = 101.0
RELATIVE_HUMIDITY_UI = 0.7
BULLET_WEIGHT = 140

SKIP_ZERO = False


def mrad_to_degree(mrad: float):
  return math.degrees(mrad / 1000)


def get_adjustment(target_distance: float, frame_per_seconds, angle: float = 0):
  shot: ShotModel = shot_service.shot_factory(
    zero_at_100y_angle, weather_condition, bullet_drag, rifle
  )
  shot_service.shoot_to_distance(shot, target_distance, frame_per_seconds)
  height_at_distance = shot_service.height_m_at_distance_m(shot, target_distance)
  margin_m = 0.00001
  lower_bound = mrad_to_degree(0)
  upper_bound = mrad_to_degree(20)

  while not -margin_m < height_at_distance < margin_m:
    if height_at_distance > 0:
      upper_bound = angle
    else:
      lower_bound = angle

    angle = (upper_bound + lower_bound) / 2.0
    shot = shot_service.shot_factory(
      angle, weather_condition, bullet_drag, rifle
    )
    shot_service.shoot_to_distance(shot, target_distance, frame_per_seconds)
    height_at_distance = shot_service.height_m_at_distance_m(shot, target_distance)
  return angle

interpolation_service = InterpolationService()
weather_condition_service = WeatherConditionService()
drag_calculator_service = DragCalculatorService(interpolation_service)
shot_service = ShotService(drag_calculator_service, interpolation_service)
zero_at_100y_angle = 0.0799622267266332

weather_condition = weather_condition_service.weather_condition_factory(
  TEMPERATURE_C, ATMOSPHERIC_PRESSURE_KPA, RELATIVE_HUMIDITY_UI
)

bullet_drag = drag_calculator_service.bullet_drag_model_factory(
  DragModels.G7, BULLET_G7_BC, 6.5, BULLET_WEIGHT
)

rifle = RifleModel(
  MUZZLE_VELOCITY_FPS, MUZZLE_DISTANCE_M, SCOPE_HEIGHT_M
)

if not SKIP_ZERO:
  zero_at_100y_angle = get_adjustment(ZERO_DISTANCE, FRAME_PER_SECONDS, zero_at_100y_angle)

angle_1000 = get_adjustment(1000, FRAME_PER_SECONDS, zero_at_100y_angle)

shot = shot_service.shot_factory(angle_1000, weather_condition, bullet_drag, rifle)
shot_service.shoot_to_distance(shot, 1010, FRAME_PER_SECONDS)

for i in np.linspace(0.0, 10.0 * YARDS_100_IN_M, 41):
  height_at_distance = shot_service.height_m_at_distance_m(shot, i)
  velocity_m_per_s = shot_service.velocity_m_per_s_at_distance_m(shot, i)
  print(f"{i/YARDS_100_IN_M * 100:{' '}{'>'}{8}.0f}y: {(height_at_distance * 39.37):{' '}{'>'}{1}0.2f}in   @ {velocity_m_per_s*3.281:{' '}{'>'}{8}.1f}fps")

fig1, ax1 = plt.subplots(2)
fig1.tight_layout()
ax1[0].plot(shot.trajectory.xm_positions, shot.trajectory.ym_positions)
ax1[0].axhline(y = 0, color = 'k')
ax1[0].axvline(x = 91.44, color = 'grey')
ax1[0].set_ylabel("height M")
ax1[0].set_xlabel("distance M")
ax1[1].plot(shot.trajectory.xm_positions, shot.trajectory.v_m_per_s_positions)
ax1[1].set_ylabel("velocity M/s")
ax1[1].set_xlabel("distance M")

fig2, ax2 = plt.subplots(3)
fig2.tight_layout()
ax2[0].plot(shot.trajectory.ts_positions, shot.trajectory.xm_positions)
ax2[0].set_ylabel("distance M")
ax2[0].set_xlabel("Time s")
ax2[1].plot(shot.trajectory.ts_positions, shot.trajectory.ym_positions)
ax2[1].set_ylabel("height M")
ax2[1].set_xlabel("Time s")
ax2[2].plot(shot.trajectory.ts_positions, shot.trajectory.v_m_per_s_positions)
ax2[2].set_ylabel("velocity M/s")
ax2[2].set_xlabel("Time s")
plt.show()
