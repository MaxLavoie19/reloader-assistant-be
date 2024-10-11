import serial

with serial.Serial("/dev/ttyUSB0", 1200) as serial_communication:
  serial_communication.write(b"?\r\n")
  last_weight = 0
  while True:
    reading = serial_communication.readline().decode()
    reading_segments = list(filter(None, reading.strip().split(' ')))
    _, info, weight_string, unit = reading_segments
    weight = float(weight_string)
    is_stable = '*' not in info
    if is_stable and last_weight != weight:
      print(weight, unit)
      last_weight = weight
