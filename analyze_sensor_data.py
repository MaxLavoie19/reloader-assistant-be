
import json
import matplotlib.pyplot as plt

from filtering.service.KalmanFilterPlotService import plot_kalman_filter_state_list


FIELD_DATA_FOLDER = "E:\Work\Shooting\ReloaderAssistant\Field data"
SESSION_NUMBER = 1


FILENAME = f"{FIELD_DATA_FOLDER}\\output_{str(SESSION_NUMBER)}_1280x720.avi.json"

with open(FILENAME) as source:
  logs = json.load(source)
  temperatures = logs["temperatures"]
  pressures = logs["pressures"]
  humidities = logs["humidities"]
  plot_kalman_filter_state_list(temperatures)
  plot_kalman_filter_state_list(pressures)
  plot_kalman_filter_state_list(humidities)
  plt.show()
