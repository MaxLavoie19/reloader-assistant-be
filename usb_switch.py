import gpiod

USB_PIN = 7

chip = gpiod.Chip('/dev/gpiochip0')
usb_line = chip.get_line(USB_PIN)
usb_line.request(consumer="USB switch", type=gpiod.LINE_REQ_DIR_OUT)
usb_line.set_value(1)
input('Switch?')
usb_line.set_value(0)
usb_line.release()
