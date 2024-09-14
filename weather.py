import board
from adafruit_bme280 import basic

i2c = board.I2C()
bme280 = basic.Adafruit_BME280_I2C(i2c, address=0x76)
print(f"{bme280.temperature}c")
print(f"{bme280.pressure}hPa")
print(f"{bme280.humidity}rh")
print(f"{bme280.overscan_temperature}rh")
