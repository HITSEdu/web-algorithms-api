from random import randint, choices
from app.models.point_type import PointType
from app.models.point import Point


def generate_tsp_grid(size: int, fullness):
    length = size - 1
    start = Point(randint(0, length), randint(0, length))
    towns = [Point(randint(0, length), randint(0, length)) for _ in range(randint(1, 4))]
    chance = fullness / 100
    while start in towns:
        start = Point(randint(0, length), randint(0, length))
    grid = [[choices([PointType.DEFAULT.value, PointType.WALL.value],
                     weights=[1 - chance, chance])[0] for _ in range(size)] for _ in range(size)]
    grid[start.x][start.y] = PointType.END.value
    for point in towns:
        grid[point.x][point.y] = PointType.CENTER.value
    return grid
