from datetime import datetime
import json
from pathlib import Path
import cv2
import board
from adafruit_bme280 import basic

from camera.model.UIStateModel import UIStateModel
from camera.service.CalibrationService import CalibrationService
from camera.service.ImageEditingService import ImageEditingService
from camera.service.UserInputService import UserInputService
from filtering.model.KalmanFilterStateModel import KalmanFilterStateModel
from filtering.service.FitnessService import FitnessService
from filtering.service.KalmanFilterService import KalmanFilterService
from reload.constant.TargetConstants import TARGET_SIZE_RATIO


def update_air_condition(
  sensor: basic.Adafruit_BME280,
  temperature_filter_state: KalmanFilterStateModel,
  pressure_filter_state: KalmanFilterStateModel,
  humidity_filter_state: KalmanFilterStateModel,
  kalman_filter_service: KalmanFilterService,
):
  now = datetime.now().timestamp()
  kalman_filter_service.kalman_filter(temperature_filter_state, sensor.temperature, 1, now)
  kalman_filter_service.kalman_filter(pressure_filter_state, sensor.pressure, 1, now)
  kalman_filter_service.kalman_filter(humidity_filter_state, sensor.humidity, 1, now)


def get_filename(size):
  counter_file_path = Path("counter.txt")
  if counter_file_path.is_file():
      counter = int(counter_file_path.read_text('utf-8'))
  else:
      counter = 0

  filename = format_file_name(counter, size)
  file_path = Path(filename)
  while file_path.is_file():
      counter += 1
      filename = format_file_name(counter, size)
      file_path = Path(filename)

  counter_file_path.write_text(f"{counter + 1}")
  return filename


def format_file_name(counter, size):
  filename = f'output_{counter}_{"x".join(map(lambda x: x.__str__(), size))}.avi'
  return filename


def get_target_rectangle(ui_state_model: UIStateModel, frame: cv2.typing.MatLike):
  target_rectangle = image_editing_service.get_centered_rectangle(
    frame, ui_state_model.target_width, ui_state_model.target_height,
  )
  offset_rectangle = [
    target_rectangle[0] + ui_state_model.left_offset,
    target_rectangle[1] + ui_state_model.top_offset,
    target_rectangle[2] + ui_state_model.left_offset,
    target_rectangle[3] + ui_state_model.top_offset,
  ]
  return offset_rectangle


def calibrate(ui_state_model: UIStateModel, frame: cv2.typing.MatLike):
  target_rectangle = get_target_rectangle(ui_state_model, frame)
  grey_frame = image_editing_service.convert_to_gray_scale(frame)
  croped_frame = image_editing_service.crop_image(grey_frame, *target_rectangle)
  image_editing_service.draw_rectangle(frame, *target_rectangle, (0,255,0), 2)
  bluriness = calibration_service.get_bluriness_level(croped_frame)
  image_editing_service.print(frame, f'bluriness {bluriness:0.4f}', (100, 100))


def record(
  ui_state_model: UIStateModel,
  frame: cv2.typing.MatLike,
  sensor: basic.Adafruit_BME280,
  temperature_filter_state: KalmanFilterStateModel,
  pressure_filter_state: KalmanFilterStateModel,
  humidity_filter_state: KalmanFilterStateModel,
  kalman_filter_service: KalmanFilterService,
):
  out.write(frame)
  croped_frame = ready(ui_state_model, frame)
  image_editing_service.add_recording_circle(croped_frame)
  update_air_condition(
    sensor,
    temperature_filter_state,
    pressure_filter_state,
    humidity_filter_state,
    kalman_filter_service,
  )
  return croped_frame


def ready(ui_state_model: UIStateModel, frame: cv2.typing.MatLike):
  target_rectangle = get_target_rectangle(ui_state_model, frame)
  croped_frame = image_editing_service.crop_image(frame, *target_rectangle)
  return croped_frame


WINDOW_NAME = "frame"
DESIRED_RESOLUTION = (1280, 960)
TARGET_WIDTH = 110
CALIBRATION_STEP = "Calibration"
READY_STEP = "Ready"
RECORDING_STEP = "Recording"

image_editing_service = ImageEditingService()
calibration_service = CalibrationService()
user_input_service = UserInputService()
fitness_service = FitnessService()
kalman_filter_service = KalmanFilterService(fitness_service)

ui_state_model = UIStateModel(
  target_width=TARGET_WIDTH,
  target_height=TARGET_WIDTH * TARGET_SIZE_RATIO,
  left_offset=0,
  top_offset=0,
  quit=False,
  is_done=False,
  current_step=CALIBRATION_STEP,
)

temperature_filter_state = KalmanFilterStateModel()
pressure_filter_state = KalmanFilterStateModel()
humidity_filter_state = KalmanFilterStateModel()

temperatures = []
pressures = []
humidities = []

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, DESIRED_RESOLUTION[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_RESOLUTION[1])
frame_shape = cap.read()[1].shape
size = (frame_shape[1], frame_shape[0])
print(size)

i2c = board.I2C()
bme280 = basic.Adafruit_BME280_I2C(i2c, address=0x76)

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while cap.isOpened():
  ret, frame = cap.read()
  if ui_state_model.current_step == CALIBRATION_STEP:
    calibrate(ui_state_model, frame)
  elif ui_state_model.current_step == READY_STEP:
    frame = ready(ui_state_model, frame)
  elif ui_state_model.current_step == RECORDING_STEP:
    frame = record(
      ui_state_model,
      frame,
      bme280,
      temperature_filter_state,
      pressure_filter_state,
      humidity_filter_state,
      kalman_filter_service,
    )
    temperatures.append(temperature_filter_state.__dict__)
    pressures.append(pressure_filter_state.__dict__)
    humidities.append(humidity_filter_state.__dict__)

  if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break

  cv2.imshow(WINDOW_NAME, frame)
  user_input_service.handle_key_press(ui_state_model)
  if ui_state_model.quit:
    break
  elif ui_state_model.is_done:
    ui_state_model.is_done = False
    if ui_state_model.current_step == CALIBRATION_STEP:
      ui_state_model.current_step = READY_STEP
    elif ui_state_model.current_step == READY_STEP:
      video_filename = get_filename(size)
      ui_state_model.current_step = RECORDING_STEP
      fourcc = cv2.VideoWriter_fourcc(*'XVID')
      out = cv2.VideoWriter(video_filename, fourcc, 20.0, size)
    elif ui_state_model.current_step == RECORDING_STEP:
      out.release()
      if len(temperatures):
        with open(f"{video_filename}.json") as destination:
          json.dump(
            { "temperatures": temperatures, "pressures": pressures, "humidities": humidities },
            destination,
          )
      temperatures = []
      pressures = []
      humidities = []
      ui_state_model.current_step = READY_STEP

out.release()
cap.release()
cv2.destroyAllWindows()
