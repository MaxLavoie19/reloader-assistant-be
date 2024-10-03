import gpiod

from gpiod.line import Direction, Value

USB_POWER_NC = 5
USB_DATA_NO = 6

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        USB_POWER_NC: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        USB_DATA_NO: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    },
) as request:
    input("Turn on data ")
    request.set_value(USB_DATA_NO, Value.ACTIVE)
    input("Turn off data ")
    request.set_value(USB_DATA_NO, Value.INACTIVE)
    input("Turn off power ")
    request.set_value(USB_POWER_NC, Value.ACTIVE)
    input("Turn on power ")
    request.set_value(USB_POWER_NC, Value.INACTIVE)
