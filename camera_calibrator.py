import cv2

from camera.service.CalibrationService import CalibrationService
from camera.service.HeadUpDisplayService import HeadUpDisplayService
from camera.service.ImageEditingService import ImageEditingService


WINDOW_NAME = "frame"
DESIRED_RESOLUTION = (1280, 960)
TARGET_SIZE_RATIO = 15.0/11.5
TARGET_WIDTH = 500
TARGET_HEIGHT = TARGET_WIDTH * TARGET_SIZE_RATIO

image_editing_service = ImageEditingService()
calibration_service = CalibrationService()
head_up_display_service = HeadUpDisplayService()

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
      frame, TARGET_WIDTH, TARGET_HEIGHT,
    )
    grey_frame = image_editing_service.convert_to_gray_scale(frame)
    croped_frame = image_editing_service.crop_image(grey_frame, *target_rectangle)
    head_up_display_service.draw_rectangle(frame, *target_rectangle, (0,255,0), 2)
    bluriness = calibration_service.get_bluriness_level(croped_frame)
    image_editing_service.print(frame, f'bluriness {bluriness:0.4f}', (100, 100))

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow(WINDOW_NAME, frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
