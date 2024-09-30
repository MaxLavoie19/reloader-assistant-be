import gpiod

from gpiod.line import Direction, Value

LINE = 4

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    request.set_value(LINE, Value.ACTIVE)
    input("Switch?")
    request.set_value(LINE, Value.INACTIVE)
