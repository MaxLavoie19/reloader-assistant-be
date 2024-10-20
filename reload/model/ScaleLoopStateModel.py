from dataclasses import dataclass, field
from typing import List, Union

@dataclass
class ScaleLoopStateModel:
  destination: str
  has_weight_changed_since_record: bool = True
  is_stable: bool = False
  unit: str = "Gn"
  reading_segments: List[str] = field(default_factory=list)
  values: List[float] = field(default_factory=list)
  last_weight: Union[float, None] = None
  min_value: Union[float, None] = None
  max_value: Union[float, None] = None
  record_length: bool = False