import serial

with serial.Serial("com1") as serial_communication:
  serial_communication.write(b"?\r\n")
  while True:
    print(serial_communication.readline())
