import serial

with serial.Serial("/dev/ttyUSB0", 1200) as serial_communication:
  serial_communication.write(b"?\r\n")
  while True:
    reading = serial_communication.readline().decode()
    reading_segments = list(filter(None, reading.strip().split(' ')))
    print(reading_segments)
