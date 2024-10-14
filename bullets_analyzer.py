import json
from typing import List
import numpy as np

import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS

from server_io.service.FileService import FileService


def draw_histogram(datapoints, nb_bins=30):
  _fig, ax = plt.subplots()
  min_value = round(np.min(datapoints), 3)
  max_value = round(np.max(datapoints), 3)
  value_range = max_value - min_value
  bin_size = round(value_range / nb_bins, 3)
  counts, bins = np.histogram(datapoints, bins=nb_bins)
  ax.hist(bins[:-1], bins, weights=counts)
  print(min_value, max_value + bin_size, bin_size)
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
desired_file = file_service.select_file("./", "bullets_", "json")

with open(desired_file) as bullets_file:
  bullets = json.load(bullets_file)

bullets_weights = list(map(lambda x: x[0], bullets))
bullets_lengths = list(map(lambda x: x[1], bullets))

clust = OPTICS(min_samples=8, min_cluster_size=8, max_eps=.01, cluster_method="dbscan")
clust.fit(np.array(bullets_lengths).reshape(-1, 1))

print(f"\nbullets weights")
print_stats(bullets_weights)
print(f"\nbullets lengths")
print_stats(bullets_lengths)
print(f"Cov: {np.cov(bullets_weights, bullets_lengths)}")

clusters = []
max_label = max(clust.labels_)
for cluster_index in range(-1, max_label + 1):
  clusters.append(
    list(sorted(
      map(lambda x: x[1], filter(lambda x: clust.labels_[x[0]] == cluster_index, enumerate(bullets_lengths)))
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
  draw_histogram(np.array(clusters[-1]))

print(f"\nlabels: {clust.labels_}")

draw_histogram(np.array(bullets_lengths))

plt.show()
