import math
import matplotlib.pyplot as plt

from ballistic.model.RifleModel import RifleModel
from ballistic.model.ShotModel import ShotModel
from ballistic.service.WeatherConditionService import WeatherConditionService
from ballistic.service.DragCalculatorService import DragCalculatorService
from ballistic.service.ShotService import ShotService
from ballistic.data.DragModels import DragModels

BERGER_6_5_140_GN_HYBRID_TARGET_G7 = 0.311
ZERO_DISTANCE = 91.44
INITIAL_VELOCITY_FPS = 2316
FRAME_PER_SECONDS = 1000.0
SCOPE_HEIGHT_M = 43.5 / 1000
MUZZLE_DISTANCE_M = .8

def mrad_to_degree(mrad: float):
  return math.degrees(mrad / 1000)

weather_condition_service = WeatherConditionService()
drag_calculator_service = DragCalculatorService()
shot_service = ShotService(drag_calculator_service)

temperature_c = 25.0
atmospheric_pressure_kpa = 101.0
relative_humidity_ui = 0.7
zero_at_100y_angle = mrad_to_degree(1.39)
adjustment = mrad_to_degree(0)
angle = zero_at_100y_angle + adjustment


weather_condition = weather_condition_service.weather_condition_factory(
  temperature_c, atmospheric_pressure_kpa, relative_humidity_ui
)

bullet_drag = drag_calculator_service.bullet_drag_model_factory(
  DragModels.G7, BERGER_6_5_140_GN_HYBRID_TARGET_G7, 6.5, 147
)

rifle = RifleModel(
  INITIAL_VELOCITY_FPS, MUZZLE_DISTANCE_M, SCOPE_HEIGHT_M
)

shot: ShotModel = shot_service.shot_factory(
  angle, weather_condition, bullet_drag, rifle
)

shot_service.shoot_to_distance(shot, ZERO_DISTANCE, FRAME_PER_SECONDS)

fig, ax = plt.subplots(2)
ax[0].plot(shot.trajectory.xm_positions, shot.trajectory.ym_positions)
ax[0].axhline(y = 0, color = 'k')
ax[0].axvline(x = 91.44, color = 'grey')
ax[1].plot(shot.trajectory.xm_positions, shot.trajectory.v_m_per_s_positions)
plt.show()
