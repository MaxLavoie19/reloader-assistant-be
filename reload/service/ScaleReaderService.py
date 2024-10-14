from datetime import datetime
import serial
import pyinputplus
from inputimeout import inputimeout, TimeoutOccurred
import json

from reload.model.ScaleLoopStateModel import ScaleLoopStateModel


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ScaleReaderService:
  def record_value(self, scale_loop_state: ScaleLoopStateModel, weight):
    nb_values = len(scale_loop_state.values)
    coordinates = self.get_coordinates(nb_values)
    last_weight = scale_loop_state.last_weight
    unit = scale_loop_state.unit
    print(f"Recorded value #{nb_values + 1} @ {coordinates}:\n{last_weight} {unit}")

    if scale_loop_state.record_length:
      length_mm = pyinputplus.inputFloat("Length (mm):")
      scale_loop_state.values.append((weight, length_mm))
      print(f"{length_mm} mm\n")
    else:
      scale_loop_state.values.append(weight)
      print()
    scale_loop_state.has_weight_changed_since_record = False
    with open(scale_loop_state.destination, 'w') as destination:
      json.dump(scale_loop_state.values, destination)

  def get_coordinates(self, index: int):
    letter_index = int((index % 100) / 10)
    letter = ALPHABET[letter_index]
    digit = int((index + 1) % 10)
    coordinates = f"{letter}{digit}"
    return coordinates

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
        if not scale_loop_state.is_stable:
          continue

        prompt = "q: Quit\n"
        last_weight = scale_loop_state.last_weight
        is_value_valid = self.is_value_valid(scale_loop_state, last_weight)
        can_record = scale_loop_state.has_weight_changed_since_record and is_value_valid
        if can_record:
          prompt = f"r: Record value {last_weight} {scale_loop_state.unit}\n{prompt}"

        try:
            user_input = inputimeout(prompt=prompt, timeout=5)
        except TimeoutOccurred:
            user_input = ''
        if user_input == 'r' and can_record:
          self.record_value(scale_loop_state, last_weight)

  def read_value(self, serial_communication: serial.Serial):
    try:
      reading = self.read_latest_line(serial_communication)
      reading_segments = list(filter(None, reading.strip().split(' ')))
    except:
      return []
    return reading_segments

  def read_latest_line(self, serial_communication: serial.Serial):
    delay = 0
    latest_line = ""
    while delay < 0.1:
      start = datetime.now()
      latest_line = serial_communication.readline()
      end = datetime.now()
      delay = (end - start).total_seconds()
    return latest_line.decode("ascii")

  def process_value(self, scale_loop_state: ScaleLoopStateModel):
    _, info, weight_string, unit = scale_loop_state.reading_segments
    weight = float(weight_string)
    scale_loop_state.is_stable = self.is_stable(info, weight)
    if not scale_loop_state.is_stable:
      return

    scale_loop_state.unit = unit

    has_weight_changed = self.has_weight_changed(scale_loop_state, weight)
    if has_weight_changed:
      scale_loop_state.last_weight = weight
      scale_loop_state.has_weight_changed_since_record = True

    is_value_valid = self.is_value_valid(scale_loop_state, weight)
    if not is_value_valid:
      self.print_correction(scale_loop_state, weight)

  def is_stable(self, info, weight):
    return '*' not in info or weight <= 1.0

  def has_weight_changed(self, scale_loop_state: ScaleLoopStateModel, weight: float):
    has_weight_changed = scale_loop_state.last_weight != weight
    return has_weight_changed

  def print_correction(self, scale_loop_state: ScaleLoopStateModel, weight: float):
    min_value = scale_loop_state.min_value
    max_value = scale_loop_state.max_value
    has_min = min_value is not None
    has_max = max_value is not None

    if not has_min or not has_max or weight <= 1:
      return

    if min_value > weight:
      print(f"+{min_value - weight}")
    elif weight > max_value:
      print(f"-{weight - max_value}")

  def is_value_valid(self, scale_loop_state: ScaleLoopStateModel, value: float):
    min_value = scale_loop_state.min_value
    max_value = scale_loop_state.max_value
    has_min = min_value is not None
    has_max = max_value is not None
    if has_min and has_max:
      is_value_valid = min_value <= value <= max_value
    else:
      is_value_valid = value > 1

    return is_value_valid

