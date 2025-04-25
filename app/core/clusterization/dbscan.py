from collections import deque
from typing import List, Tuple
from app.models.point import Point
from app.core.clusterization.euclidean import euclidean


def region_query(points: List[Point], p: Point, eps: float) -> List[Point]:
    return [q for q in points if euclidean(p, q) <= eps]


def expand_cluster(points: List[Point], neighbors: List[Point], cluster: List[Point],
                   visited: set, eps: float, min_pts: int) -> None:
    queue = deque(neighbors)
    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            current_neighbors = region_query(points, current, eps)
            if len(current_neighbors) >= min_pts:
                queue.extend(q for q in current_neighbors if q not in visited)
        if current not in cluster:
            cluster.append(current)


def dbscan(points, eps: float, min_pts: int) -> Tuple[List[List[Point]], List[Point]]:
    clusters: List[List[Point]] = []
    visited: set = set()
    noise: List[Point] = []
    for point in points:
        if point in visited:
            continue
        visited.add(point)
        neighbors = region_query(points, point, eps)
        if len(neighbors) < min_pts:
            noise.append(point)
        else:
            new_cluster: List[Point] = []
            expand_cluster(points, neighbors, new_cluster, visited, eps, min_pts)
            clusters.append(new_cluster)
    return clusters, noise
