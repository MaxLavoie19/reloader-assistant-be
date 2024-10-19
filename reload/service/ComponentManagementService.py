from typing import List
import numpy as np

from sklearn.cluster import OPTICS


class ComponentManagementService:
  def clusterize_components(self, components: List, max_eps, cluser_size: 8):
    component_array = np.array(components).reshape(-1, 1)
    clust = OPTICS(
      min_samples=cluser_size,
      min_cluster_size=cluser_size,
      max_eps=max_eps,
      cluster_method="dbscan"
    )
    clust.fit(component_array)

    clusters = []
    max_label = max(clust.labels_)
    for cluster_label in range(max_label + 1):
      cluster = list(sorted(map(
        lambda x: x, filter(lambda x: clust.labels_[x[0]] == cluster_label, enumerate(components))
      )))
      clusters.append(cluster)
      if len(clusters[-1]) <= 1:
        continue
    return clusters

  def split_cluster(self, cluster: List, sub_cluster_size=8):
    sub_clusters: List[List[float]] = []
    for i, element in enumerate(cluster):
      if i % sub_cluster_size == 0:
        sub_clusters.append([])
      sub_clusters[-1].append(element)
    if len(sub_clusters[-1]) < sub_cluster_size:
      sub_clusters.pop()
    return sub_clusters

  def sort_into_competition_bins(self, components: list, max_eps: float, bin_size: float=8):
    clusters = self.clusterize_components(
      components, max_eps=max_eps, cluser_size=bin_size
    )
    bins = []
    for cluster in clusters:
      bins += self.split_cluster(cluster, bin_size)
    sorted_bins = sorted(bins, key=lambda x: np.std(x, 0)[1])
    return sorted_bins
