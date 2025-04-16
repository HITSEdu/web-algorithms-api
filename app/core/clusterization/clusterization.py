import random
from typing import List, Tuple
from app.models.color_type import ColorType
from app.models.point import Point
from app.models.point_type import PointType
from app.core.clusterization.euclidean import euclidean
from app.core.clusterization.silhouette_method import calculate_silhouette


def find_points(canvas: List[List[int]]) -> List[Point]:
    n: int = len(canvas)
    points: List[Point] = []
    for x in range(n):
        for y in range(n):
            if canvas[x][y] == PointType.WALL.value:
                points.append(Point(x, y))
    return points


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


def k_means(canvas: List[List[int]], k: int) -> Tuple[List[List[Point]], List[Point]]:
    eps = 32
    points = find_points(canvas)
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


def build_canvas(canvas: List[List[int]], k: int, clusters: List[List[Point]],
                 centroids: List[List[Point]]) -> List[List[int]]:
    n = len(canvas)
    colors: List[ColorType] = [ColorType.ORANGE, ColorType.BLUE, ColorType.GREEN,
                               ColorType.PURPLE, ColorType.YELLOW, ColorType.PINK]
    new_canvas = []
    matrix = [[0] * n for _ in range(n)]
    for color in range(k):
        for cluster in clusters[color]:
            matrix[cluster.x][cluster.y] = colors[color].value

    for center in centroids:
        matrix[center.x][center.y] = int(f"{matrix[center.x][center.y]}{PointType.CENTER.value}")
    new_canvas = matrix
    return new_canvas


def check_canvas(canvas: List[List[int]]) -> bool:
    n = len(canvas)
    for x in range(n):
        for y in range(n):
            if canvas[x][y] != PointType.WALL.value:
                return True
    return False


def clusterization(canvas: List[List[int]]):
    if not check_canvas(canvas):
        return {
            "k": 2,
            "canvas": [[0] * len(canvas) for _ in range(len(canvas))],
            "c": 0,
        }
    m = {}
    for k in range(2, 6 + 1):
        clusters, centriods = k_means(canvas, k)
        c = calculate_silhouette(clusters)
        new_canvas = build_canvas(canvas, k, clusters, centriods)
        m.update({k: {
            "k": k,
            "canvas": new_canvas,
            "c": c,
            "type": "k-means",
        }})
    return m
