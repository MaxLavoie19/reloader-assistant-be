import serial
import keyboard
import json

is_new_value = True
values_grid = [[]]
with serial.Serial("/dev/ttyUSB0", 1200) as serial_communication:
  serial_communication.write(b"?\r\n")
  last_weight = 0
  while True:
    reading = serial_communication.readline().decode()
    reading_segments = list(filter(None, reading.strip().split(' ')))
    if len(reading_segments) != 4:
      continue

    _, info, weight_string, unit = reading_segments
    weight = float(weight_string)
    is_stable = '*' not in info

    if is_stable and last_weight != weight:
      print(weight, unit)
      last_weight = weight
      is_new_value = True

    is_enter_pressed = keyboard.is_pressed('enter')
    if is_enter_pressed and is_new_value:
      is_new_value = False
      latest_row = values_grid[-1]
      latest_row.append(weight)
      if len(latest_row) == 10:
        values_grid.append([])

    is_q_pressed = keyboard.is_pressed('q')
    if is_q_pressed:
      break

with open(f"bullet.json", 'w') as destination:
  json.dump(values_grid, destination)
