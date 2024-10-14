import json
from typing import Dict, List, Tuple

from sklearn.cluster import OPTICS
import numpy as np

from reload.service.TrayService import TrayService
from server_io.service.FileService import FileService


tray_service = TrayService()
file_service = FileService()

desired_file = file_service.select_file("./", "brasses_", "json")

with open(desired_file) as brasses_file:
  brasses = json.load(brasses_file)

clust = OPTICS(min_samples=8, min_cluster_size=8, max_eps=.75, cluster_method="dbscan")
clust.fit(np.array(brasses).reshape(-1, 1))

cluster_dict: Dict[int, List[Tuple[int, float]]] = {}
for index_weight in enumerate(brasses):
  index, brass_weight = index_weight
  cluster_label = clust.labels_[index]
  if cluster_label == -1:
    continue

  if cluster_label not in cluster_dict:
    cluster_dict[cluster_label] = []
  cluster = cluster_dict[cluster_label]
  cluster.append(index_weight)

cases = []
case_index = 0
for cluster_label, cluster in cluster_dict.items():
  min_value = min(map(lambda x: x[1], cluster))
  max_value = max(map(lambda x: x[1], cluster))
  cluster_coordinates = sorted(map(lambda x: tray_service.get_coordinates(x[0]), cluster))
  print(f"Cluster #{cluster_label}: {min_value}-{max_value}")
  print(", ".join(cluster_coordinates))
  sorted_cluster = sorted(cluster, key=lambda x: x[1])
  case = []
  cluster_case_index = 0
  for index_weight in sorted_cluster:
    case.append(index_weight)
    if len(case) == 8:
      weights = sorted(map(lambda x: x[1], case))
      coordinates = sorted(map(lambda x: tray_service.get_coordinates(x[0]), case))
      coordinates_string = ", ".join(coordinates)
      case_range = round(weights[-1]-weights[0], 2)
      case_info = f"#{case_index} {weights[0]}-{weights[-1]} {case_range}"
      print(f"    Case {case_info}:\t{coordinates_string}")
      if cluster_case_index % 3 == 0 and cluster_case_index > 0:
        print()
      cluster_case_index += 1
      case_index += 1
      case = []
  print()
