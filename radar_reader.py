from pprint import pprint
import time
from os import listdir
from os.path import isfile, join

import gpiod
from gpiod.line import Direction, Value
from garmin_fit_sdk import Decoder, Stream

from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService
from server_io.service.UserFolderService.UserFolderService import UserFolderService
from session.mapper.FitFileToRadarShotMapper import fit_file_to_radar_shots_mapper

USB_POWER_NC = 5
USB_DATA_NO = 6

user_folder_service = UserFolderService()
json_serializer_service = JsonSerializerService(user_folder_service)


def get_fit_file_paths(garmin_path: str, user_file_path: str):
  file_paths = [
    isfile(join(garmin_path, f))
    for f in listdir(garmin_path)
    if isfile(join(garmin_path, f)) and not isfile(join(user_file_path, f)) and ".fit" in f
  ]

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

  blocs_folder = user_folder_service.get_shooting_blocs_folder("maxlavoie1960@hotmail.com")
  file_paths = get_fit_file_paths("/media/pi5user/GARMIN/Garmin/Shot_sessions/", blocs_folder)

  for file in file_paths:
    stream = Stream.from_file(file)
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    shots = fit_file_to_radar_shots_mapper(messages)
    shot_dicts = []
    for shot in shots:
        shot_dicts.append(shot.__dict__)

    json_serializer_service.dump_radar_readings(file, shot_dicts)

  print("Disconnecting radar")
  request.set_value(USB_DATA_NO, Value.INACTIVE)
  request.set_value(USB_POWER_NC, Value.ACTIVE)
  time.sleep(1)

  print("Turning on power ")
  request.set_value(USB_POWER_NC, Value.INACTIVE)
