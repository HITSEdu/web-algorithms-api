import random
from typing import List, Tuple
from app.core.clusterization.euclidean import euclidean
from app.models.point import Point


def init_centroids(k: int, points: List[Point]) -> List[Point]:
    centroids = []
    centroids.append(random.choice(points))

    for _ in range(1, k):
        distances = []
        for p in points:
            min_dist = min(euclidean(p, c) for c in centroids)
            distances.append(min_dist ** 2)
        total = sum(distances)
        probs = [d / total for d in distances if total]
        next_point = random.choices(points, weights=probs, k=1)[0]
        centroids.append(next_point)
    return centroids


def update_centroids(clusters: List[List[Point]], points: List[Point]) -> List[Point]:
    new_centroids: List[Point] = []
    largest_cluster = max(clusters, key=len) if clusters else []
    for cluster in clusters:
        if cluster:
            x = sum(p.x for p in cluster) // len(cluster)
            y = sum(p.y for p in cluster) // len(cluster)
            closest_point = min(points, key=lambda p: euclidean(Point(x, y), p))
            new_centroids.append(closest_point)
        else:
            if largest_cluster:
                new_centroids.append(random.choice(largest_cluster)
                                     if largest_cluster else random.choice(points))
            else:
                new_centroids.append(Point(0, 0))
    return new_centroids


def k_means(points: List[Point], k: int) -> Tuple[List[List[Point]], List[Point]]:
    eps = 32
    centroids = init_centroids(k, points)
    clusters: List[List[Point]] = []

    for _ in range(eps):
        clusters = [[] for _ in range(k)]
        for point in points:
            distance = min(euclidean(point, center) for center in centroids)
            cluster_idx = [euclidean(point, center) for center in centroids].index(distance)
            clusters[cluster_idx].append(point)
        centroids = []
        centroids = update_centroids(clusters, points)
    return clusters, centroids
