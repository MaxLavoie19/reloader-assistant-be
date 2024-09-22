import cv2
import keyboard

from reload.constant.TargetConstants import TARGET_SIZE_RATIO
from camera.model.UIStateModel import UIStateModel

UP_ARROW_CODE = 2490368
DOWN_ARROW_CODE = 2621440
LEFT_ARROW_CODE = 2424832
RIGHT_ARROW_CODE = 2555904
ENTER_CODE = 13


class UserInputService:
  def handle_key_press(self, ui_state_model: UIStateModel):
    key_input = cv2.waitKeyEx(1)
    if key_input == -1:
      return
    elif key_input == ord('+'):
      ui_state_model.target_width += 1
      ui_state_model.target_height = ui_state_model.target_width * TARGET_SIZE_RATIO
      return
    elif key_input == ord('-'):
      ui_state_model.target_width -= 1
      ui_state_model.target_height = ui_state_model.target_width * TARGET_SIZE_RATIO
      return

    is_shift_pressed = keyboard.is_pressed('shift')
    if is_shift_pressed:
        offset_increment = 5
    else:
        offset_increment = 1

    if key_input == ord('q'):
        ui_state_model.quit = True
    elif key_input == UP_ARROW_CODE:
        ui_state_model.top_offset -= offset_increment
    elif key_input == DOWN_ARROW_CODE:
        ui_state_model.top_offset += offset_increment
    elif key_input == LEFT_ARROW_CODE:
        ui_state_model.left_offset -= offset_increment
    elif key_input == RIGHT_ARROW_CODE:
        ui_state_model.left_offset += offset_increment
    elif key_input == ENTER_CODE:
       ui_state_model.is_done = True
    elif key_input != -1:
        print(key_input)
