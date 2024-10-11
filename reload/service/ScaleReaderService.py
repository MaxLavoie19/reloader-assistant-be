from typing import List, Union
import serial
import keyboard

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel


class ScaleReaderService:
  def record_value(self, scale_loop_state: ScaleLoopStateModel, weight):
    if len(scale_loop_state.values_grid) == 0:
      scale_loop_state.values_grid.append([])

    latest_row = scale_loop_state.values_grid[-1]
    if len(latest_row) == 10:
      scale_loop_state.values_grid.append([])
      latest_row = scale_loop_state.values_grid[-1]

    latest_row.append(weight)

  def record_grid(self, min_value:Union[float, None]=None, max_value:Union[float, None]=None):
    scale_loop_state = ScaleLoopStateModel(min_value=min_value, max_value=max_value)
    with serial.Serial("/dev/ttyUSB0", 1200) as serial_communication:
      serial_communication.write(b"?\r\n")
      scale_loop_state.last_weight = 0
      is_q_pressed = False
      while not is_q_pressed:
        scale_loop_state.reading_segments = self.read_value(serial_communication)

        scale_loop_state.last_weight = self.process_value(scale_loop_state)
        is_q_pressed = keyboard.is_pressed('q')

    return scale_loop_state.values_grid

  def read_value(self, serial_communication: serial.Serial):
    reading = serial_communication.readline().decode()
    reading_segments = list(filter(None, reading.strip().split(' ')))
    return reading_segments

  def process_value(self, scale_loop_state: ScaleLoopStateModel):
    if len(scale_loop_state.reading_segments) != 4:
      return

    _, info, weight_string, unit = scale_loop_state.reading_segments
    weight = float(weight_string)
    is_stable = '*' not in info

    has_weight_changed = scale_loop_state.last_weight != weight
    if is_stable and has_weight_changed:
      print(f"{scale_loop_state.last_weight} {unit} -> {weight} {unit}")
      scale_loop_state.last_weight = weight
      scale_loop_state.has_weight_changed_since_record = True

    is_value_valid = (
        scale_loop_state.min_value is None
      ) or (
        scale_loop_state.max_value is None
      ) or (
        scale_loop_state.min_value <= weight <= scale_loop_state.max_value
      )

    is_enter_pressed = keyboard.is_pressed('enter')
    if is_enter_pressed and is_value_valid and scale_loop_state.has_weight_changed_since_record:
      scale_loop_state.has_weight_changed_since_record = False
      self.record_value(scale_loop_state, weight)
