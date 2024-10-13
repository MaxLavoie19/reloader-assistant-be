import serial
import pyinputplus
from inputimeout import inputimeout, TimeoutOccurred

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel


class ScaleReaderService:
  def record_value(self, scale_loop_state: ScaleLoopStateModel, weight):
    if len(scale_loop_state.values_grid) == 0:
      scale_loop_state.values_grid.append([])

    latest_row = scale_loop_state.values_grid[-1]
    if len(latest_row) == 10:
      scale_loop_state.values_grid.append([])
      latest_row = scale_loop_state.values_grid[-1]
    print(f"Recorded:\n{scale_loop_state.last_weight} {scale_loop_state.unit}")

    if scale_loop_state.record_length:
      length_mm = pyinputplus.inputFloat("Length (mm):")
      latest_row.append((weight, length_mm))
      print(f"{length_mm} mm\n")
    else:
      latest_row.append(weight)
      print()
    scale_loop_state.has_weight_changed_since_record = False

  def record_grid(self, scale_loop_state: ScaleLoopStateModel):
    can_record = False
    with serial.Serial("/dev/ttyUSB0", 1200) as serial_communication:
      serial_communication.write(b"?\r\n")
      scale_loop_state.last_weight = 0
      user_input = ''
      while user_input != 'q':
        scale_loop_state.reading_segments = self.read_value(serial_communication)
        if len(scale_loop_state.reading_segments) != 4:
          continue

        self.process_value(scale_loop_state)
        prompt = "q: Quit\n"
        last_weight = scale_loop_state.last_weight
        is_value_valid = self.is_value_valid(scale_loop_state, last_weight)
        can_record = scale_loop_state.has_weight_changed_since_record and is_value_valid
        if can_record:
          prompt = f"r: Record value {last_weight} {scale_loop_state.unit}\n{prompt}"

        try:
            user_input = inputimeout(prompt=prompt, timeout=3)
        except TimeoutOccurred:
            user_input = ''
        if user_input == 'r' and can_record:
          self.record_value(scale_loop_state, last_weight)

    return scale_loop_state.values_grid

  def read_value(self, serial_communication: serial.Serial):
    try:
      serial_communication.readlines()  # read all lines since last reading then wait for next reading
      reading = serial_communication.readline().decode("ascii")
      reading_segments = list(filter(None, reading.strip().split(' ')))
    except:
      return []
    return reading_segments

  def process_value(self, scale_loop_state: ScaleLoopStateModel):
    _, info, weight_string, unit = scale_loop_state.reading_segments
    weight = float(weight_string)
    is_stable = self.is_stable(info, weight)
    print(f"is_stable {is_stable}, '*' not in {info} or {weight} <= 1.0")
    scale_loop_state.unit = unit

    has_weight_changed = self.has_weight_changed(scale_loop_state, weight)
    if is_stable and has_weight_changed:
      scale_loop_state.last_weight = weight
      scale_loop_state.has_weight_changed_since_record = True

    is_value_valid = self.is_value_valid(scale_loop_state, weight)
    if is_stable and not is_value_valid:
      self.print_correction(scale_loop_state, weight)

  def is_stable(self, info, weight):
    return '*' not in info or weight <= 1.0

  def has_weight_changed(self, scale_loop_state: ScaleLoopStateModel, weight: float):
    has_weight_changed = scale_loop_state.last_weight != weight
    return has_weight_changed

  def print_correction(self, scale_loop_state: ScaleLoopStateModel, weight: float):
    if scale_loop_state.min_value > weight:
      print(f"+{scale_loop_state.min_value - weight}")
    elif weight > scale_loop_state.max_value:
      print(f"-{weight - scale_loop_state.max_value}")

  def is_value_valid(self, scale_loop_state: ScaleLoopStateModel, value: float):
    min_value = scale_loop_state.min_value
    max_value = scale_loop_state.max_value
    has_min = min_value is not None
    has_max = max_value is not None
    if has_min and has_max:
      is_value_valid = min_value <= value <= max_value
    else:
      is_value_valid = True

    return is_value_valid

