from typing import List
from app.core.clusterization.euclidean import euclidean
from app.models.point import Point


def calculate_silhouette(clusters: List[List[Point]]) -> float:
    scores = []
    num_clusters = len(clusters)

    for i in range(num_clusters):
        cluster = clusters[i]
        if len(cluster) < 2:
            continue

        for point in cluster:
            a = sum(euclidean(point, other) for other in cluster
                    if other != point) / (len(cluster) - 1) if len(cluster) > 1 else 0
            b = float("inf")
            for j in range(num_clusters):
                if i == j or not clusters[j]:
                    continue
                avg_dist = sum(euclidean(point, other) for other in clusters[j]) / len(clusters[j])
                b = min(b, avg_dist)
            s = (b - a) / max(a, b)
            scores.append(s)
    return sum(scores) / len(scores) if scores else -1
