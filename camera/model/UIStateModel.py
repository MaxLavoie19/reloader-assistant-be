from dataclasses import dataclass


@dataclass
class UIStateModel:
  target_width: int
  target_height: int
  top_offset: int
  left_offset: int
  quit: bool
  is_done: bool
  current_step: str
