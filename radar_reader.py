import time
from os import listdir
from os.path import isfile, join

import gpiod
from gpiod.line import Direction, Value
from garmin_fit_sdk import Decoder, Stream

from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService
from server_io.service.UserFolderService.UserFolderService import UserFolderService
from server_io.service.FileService import FileService
from session.mapper.FitFileToRadarShotMapper import fit_file_to_radar_shots_mapper

USB_POWER_NC = 5
USB_DATA_NO = 6

user_folder_service = UserFolderService()
json_file_service = FileService()
json_serializer_service = JsonSerializerService(json_file_service, user_folder_service)


def get_fit_file_paths(garmin_path: str, user_file_path: str):
  file_paths = [
    join(garmin_path, f)
    for f in listdir(garmin_path)
    if isfile(join(garmin_path, f)) and not isfile(join(user_file_path, f)) and ".fit" in f
  ]
  print(file_paths)
  return file_paths


with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        USB_POWER_NC: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        USB_DATA_NO: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    },
) as request:
  print("Turning on data")
  request.set_value(USB_POWER_NC, Value.INACTIVE)
  request.set_value(USB_DATA_NO, Value.ACTIVE)
  time.sleep(10)

  blocs_folder = user_folder_service.get_shooting_blocs_folder("maxlavoie1960@hotmail.com")
  file_paths = get_fit_file_paths("/media/pi5user/GARMIN/Garmin/Shot_Sessions/", blocs_folder)

  for file_path in file_paths:
    stream = Stream.from_file(file_path)
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    shots = fit_file_to_radar_shots_mapper(messages)
    if len(shots) == 0:
       continue

    shot_dicts = []
    for shot in shots:
        shot_dicts.append(shot.__dict__)

    json_serializer_service.dump_radar_readings(file_path, shot_dicts)

  print("Disconnecting radar")
  request.set_value(USB_DATA_NO, Value.INACTIVE)
  request.set_value(USB_POWER_NC, Value.ACTIVE)
  time.sleep(1)

  print("Turning on power ")
  request.set_value(USB_POWER_NC, Value.INACTIVE)
