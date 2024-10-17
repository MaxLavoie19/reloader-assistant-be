import math

from ballistic.model.WeatherConditionModel import WeatherConditionModel


WATER_MOLAR_MASS_KG_PER_MOL = 0.018016
DRY_AIR_MOLAR_MASS_KG_PER_MOL = 0.0289652
UNIVERSAL_GAS_CONSTANT = 8.31446261815324
BOLTZMANN_CONSTANT = 1.380649e-23
MOLE = 6.02214076e23
AIR_MOLAR_MASS_KG = 28.96 / 1000
AVERAGE_AIR_ATOM_MASS = AIR_MOLAR_MASS_KG / MOLE
AIR_ADIABATIC_INDEX = 1.4
SPEED_OF_SOUND_PER_C = AIR_ADIABATIC_INDEX * BOLTZMANN_CONSTANT / AVERAGE_AIR_ATOM_MASS

class WeatherConditionService:
  def weather_condition_factory(
    self, temperature_c: float, atmospheric_pressure_kpa: float, relative_humidity_ui: float
  ) -> WeatherConditionModel:
    air_density = self.air_density(temperature_c, atmospheric_pressure_kpa, relative_humidity_ui)
    temperature_k = self.temperature_k(temperature_c)
    speed_of_sound_m_per_s = self.speed_of_sound_m_per_s(temperature_k)
    weather_condition = WeatherConditionModel(
      temperature_c=temperature_c,
      temperature_k=temperature_k,
      relative_humidity_ui=relative_humidity_ui,
      atmospheric_pressure_kpa=atmospheric_pressure_kpa,
      air_density=air_density,
      speed_of_sound_m_per_s=speed_of_sound_m_per_s,
    )
    return weather_condition

  def air_density(self, temperature_c, pressure_kpa, relative_humidity_ui):
    temperature_k = self.temperature_k(temperature_c)
    water_saturation_vapor_pressure_kpa = self.teten_Equation(temperature_c)
    water_vapor_pressure = relative_humidity_ui * water_saturation_vapor_pressure_kpa
    dividend = pressure_kpa * DRY_AIR_MOLAR_MASS_KG_PER_MOL + \
      water_vapor_pressure * WATER_MOLAR_MASS_KG_PER_MOL
    divisor = UNIVERSAL_GAS_CONSTANT * temperature_k
    air_density = dividend / divisor
    return air_density * 1000

  def temperature_k(self, temperature_c: float):
    return temperature_c + 273.15

  def teten_Equation(self, temperature_c):
    water_saturation_vapor_pressure_kpa = 0.61078 * math.exp(17.27 * temperature_c / (temperature_c + 237.3))
    return water_saturation_vapor_pressure_kpa

  def speed_of_sound_m_per_s(self, temperature_k):
    speed_of_sound_m_per_s = math.sqrt(
      temperature_k * SPEED_OF_SOUND_PER_C
    )
    return speed_of_sound_m_per_s
