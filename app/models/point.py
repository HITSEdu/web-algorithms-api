from typing import Optional


class Point:
    def __init__(self, x: int, y: int, _id: Optional[int] = None):
        self.id = _id
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
