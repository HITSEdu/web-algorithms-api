from app.models.point import Point


def euclidean(p1: Point, p2: Point) -> int:
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
