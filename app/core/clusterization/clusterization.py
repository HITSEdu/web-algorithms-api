from typing import List
from app.models.color_type import ColorType
from app.models.point import Point
from app.models.point_type import PointType
from app.core.clusterization.silhouette_method import calculate_silhouette
from app.core.clusterization.k_means import k_means
from app.core.clusterization.dbscan import dbscan


def find_points(canvas: List[List[int]]) -> List[Point]:
    n: int = len(canvas)
    points: List[Point] = []
    for x in range(n):
        for y in range(n):
            if canvas[x][y] == PointType.WALL.value:
                points.append(Point(x, y))
    return points


def build_canvas(n: int, k: int, clusters: List[List[Point]],
                 centroids: List[List[Point]]) -> List[List[int]]:
    colors: List[ColorType] = [ColorType.ORANGE, ColorType.BLUE, ColorType.GREEN,
                               ColorType.PURPLE, ColorType.YELLOW, ColorType.PINK]
    matrix = [[0] * n for _ in range(n)]
    for color in range(k):
        for cluster in clusters[color]:
            matrix[cluster.x][cluster.y] = colors[color].value

    for center in centroids:
        matrix[center.x][center.y] = int(f"{matrix[center.x][center.y]}{PointType.CENTER.value}")
    return matrix


def make_k_means_json(points: List[Point], size: int):
    num_of_clusters = min(6, len(points))
    k_means_data = []
    for k in range(2, num_of_clusters + 1):
        clusters, centriods = k_means(points, k)
        c = calculate_silhouette(clusters)
        new_canvas = build_canvas(size, k, clusters, centriods)
        k_means_data.append({
            "k": k,
            "canvas": new_canvas,
            "c": c,
        })
    return k_means_data


def make_dbscan_json(points: List[Point], size: int):
    clusters, noise = dbscan(points, int(size**0.5)*2, int(size**0.5))
    new_canvas = build_canvas(size, len(clusters), clusters, noise)
    return [{
        "k": len(clusters),
        "canvas": new_canvas,
        "c": 0,
        }]


def clusterization(canvas: List[List[int]]):
    points = find_points(canvas)
    size = len(canvas)
    if len(points) < 2:
        return {}, -1
    response = {
        "k-means": make_k_means_json(points, size),
        "DBSCAN": make_dbscan_json(points, size),
    }
    return response, 1
