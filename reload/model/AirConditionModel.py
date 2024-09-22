from dataclasses import dataclass
from datetime import datetime


@dataclass
class AirConditionModel:
  timestamp: datetime
  temperature: float
  pressure: float
  humidity: float
