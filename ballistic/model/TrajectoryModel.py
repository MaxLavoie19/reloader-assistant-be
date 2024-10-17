from dataclasses import dataclass, field
from typing import List

@dataclass
class TrajectoryModel:
  xm_positions: List[float] = field(default_factory=list)
  ym_positions: List[float] = field(default_factory=list)
  ts_positions: List[float] = field(default_factory=list)
  v_m_per_s_positions: List[float] = field(default_factory=list)
