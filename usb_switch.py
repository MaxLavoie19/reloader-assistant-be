import gpiod

USB_PIN = 4

chip = gpiod.Chip('/dev/gpiochip0')
led_line = chip.get_line(USB_PIN)
led_line.request(consumer="USB switch", type=gpiod.LINE_REQ_DIR_OUT)
led_line.set_value(1)
input('Switch?')
led_line.set_value(0)
led_line.release()
