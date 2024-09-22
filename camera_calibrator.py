import cv2

from camera.model.UIStateModel import UIStateModel
from camera.service.CalibrationService import CalibrationService
from camera.service.HeadUpDisplayService import HeadUpDisplayService
from camera.service.ImageEditingService import ImageEditingService
from camera.service.UserInputService import UserInputService
from reload.constant.TargetConstants import TARGET_SIZE_RATIO


WINDOW_NAME = "frame"
DESIRED_RESOLUTION = (1280, 960)
TARGET_WIDTH = 110

# TODO: move target using arrows?

image_editing_service = ImageEditingService()
calibration_service = CalibrationService()
head_up_display_service = HeadUpDisplayService()
user_input_service = UserInputService()

ui_state_model = UIStateModel(
  target_width=TARGET_WIDTH,
  target_height=TARGET_WIDTH * TARGET_SIZE_RATIO,
  left_offset=0,
  top_offset=0,
  quit=False,
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, DESIRED_RESOLUTION[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_RESOLUTION[1])
frame_shape = cap.read()[1].shape
size = (frame_shape[1], frame_shape[0])
print(size)

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    ret, frame = cap.read()

    target_rectangle = image_editing_service.get_centered_rectangle(
      frame, ui_state_model.target_width, ui_state_model.target_height,
    )

    offset_rectangle = [
      target_rectangle[0] + ui_state_model.left_offset,
      target_rectangle[1] + ui_state_model.top_offset,
      target_rectangle[2] + ui_state_model.left_offset,
      target_rectangle[3] + ui_state_model.top_offset,
    ]
    grey_frame = image_editing_service.convert_to_gray_scale(frame)
    croped_frame = image_editing_service.crop_image(grey_frame, *offset_rectangle)
    head_up_display_service.draw_rectangle(frame, *offset_rectangle, (0,255,0), 2)
    bluriness = calibration_service.get_bluriness_level(croped_frame)
    image_editing_service.print(frame, f'bluriness {bluriness:0.4f}', (100, 100))

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow(WINDOW_NAME, frame)
    user_input_service.handle_key_press(ui_state_model)
    if ui_state_model.quit:
        break

cap.release()
cv2.destroyAllWindows()
