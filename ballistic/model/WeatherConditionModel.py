from dataclasses import dataclass

@dataclass
class WeatherConditionModel:
  temperature_c: float
  temperature_k: float
  relative_humidity_ui: float
  atmospheric_pressure_kpa: float
  air_density: float
  speed_of_sound_m_per_s: float
