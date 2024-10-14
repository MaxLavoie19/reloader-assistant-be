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
for cluster_label, cluster in cluster_dict.items():
  min_value = min(map(lambda x: x[1], cluster))
  max_value = max(map(lambda x: x[1], cluster))
  cluster_coordinates = sorted(map(lambda x: tray_service.get_coordinates(x[0]), cluster))
  print(f"{cluster_label}: {min_value}-{max_value}")
  print(", ".join(cluster_coordinates))
  sorted_cluster = sorted(cluster, key=lambda x: x[1])
  case = []
  for index_weight in sorted_cluster:
    case.append(index_weight)
    if len(case) == 8:
      coordinates = sorted(map(lambda x: tray_service.get_coordinates(x[0]), case))
      print(", ".join(coordinates))
      case = []
  print()
