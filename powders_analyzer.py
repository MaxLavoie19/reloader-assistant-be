import json
from typing import List
import numpy as np

import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS

from server_io.service.FileService import FileService


def draw_histogram(datapoints, nb_bins=30):
  _fig, ax = plt.subplots()
  min_value = round(np.min(datapoints), 2)
  max_value = round(np.max(datapoints), 2)
  value_range = max_value - min_value
  bin_size = max(round(value_range / nb_bins, 2), 0.001)
  counts, bins = np.histogram(datapoints, bins=nb_bins)
  ax.hist(bins[:-1], bins, weights=counts)
  ax.set_xticks(np.arange(min_value, max_value + bin_size, bin_size))


def print_stats(datapoints):
  print(f"sample size: {len(datapoints)}")
  min_value = np.min(datapoints)
  max_value = np.max(datapoints)
  print(f"min: {min_value}")
  print(f"max: {max_value}")
  print(f"range: {max_value - min_value}")
  print(f"mean: {np.mean(datapoints)}")
  print(f"std: {np.std(datapoints)}")


def split_cluster(cluster, sub_cluster_size=8):
  sub_clusters: List[List[float]] = []
  for i, element in enumerate(cluster):
    if i % sub_cluster_size == 0:
      sub_clusters.append([])
    sub_clusters[-1].append(element)
  if len(sub_clusters[-1]) < sub_cluster_size:
    sub_clusters.pop()
  return sub_clusters

file_service = FileService()

desired_file = file_service.select_file("./", "powders_", "json")

with open(desired_file) as powders_file:
  powders = json.load(powders_file)

clust = OPTICS(min_samples=8, min_cluster_size=8, max_eps=0.003, cluster_method="dbscan")
clust.fit(np.array(powders).reshape(-1, 1))

print(f"\npowders")
print_stats(powders)

clusters = []
max_label = max(clust.labels_)
for cluster_index in range(-1, max_label + 1):
  clusters.append(
    list(sorted(
      map(lambda x: x[1], filter(lambda x: clust.labels_[x[0]] == cluster_index, enumerate(powders)))
    ))
  )
  if len(clusters[-1]) <= 1:
    continue
  print(f"\n{cluster_index}")
  print_stats(clusters[-1])
  print(clusters[-1])
  sub_clusters = split_cluster(clusters[-1])
  for sub_cluster in sub_clusters:
    print()
    print_stats(sub_cluster)
  draw_histogram(clusters[-1], nb_bins=15)

print(f"\nlabels: {clust.labels_}")

draw_histogram(powders, nb_bins=30)

plt.show()
