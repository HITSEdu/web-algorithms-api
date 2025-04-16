from heapq import heappush, heappop
from random import choice, randrange, random, shuffle
from collections import deque
from app.models.point_type import PointType
from app.models.point import Point


DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]


def in_bounds(x, y, size):
    return 0 <= x < size and 0 <= y < size


def is_connected(grid, start, end, size):
    visited = [[False] * size for _ in range(size)]
    q = deque([start])
    visited[start[0]][start[1]] = True
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, size) and not visited[nx][ny] and grid[nx][ny] in (0, 3):
                visited[nx][ny] = True
                q.append((nx, ny))
    return False


def generate_maze(size: int, fullness):
    grid = [[PointType.WALL.value for _ in range(size)] for _ in range(size)]

    start = Point(randrange(1, size, 2), randrange(1, size, 2))
    grid[start.x][start.y] = PointType.DEFAULT.value
    walls = []

    for dx, dy in DIRS:
        nx, ny = start.x + dx, start.y + dy
        if in_bounds(nx, ny, size):
            heappush(walls, (random(), start, Point(nx, ny)))

    while walls:
        _, from_cell, to_cell = heappop(walls)
        x, y = to_cell.x, to_cell.y
        if not in_bounds(x, y, size) or grid[x][y] == PointType.DEFAULT.value:
            continue

        wall_x = (from_cell.x + x) // 2
        wall_y = (from_cell.y + y) // 2

        grid[wall_x][wall_y] = PointType.DEFAULT.value
        grid[x][y] = PointType.DEFAULT.value

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, size) and grid[nx][ny] == 1:
                heappush(walls, (random(), Point(x, y), Point(nx, ny)))

    free = [(x, y) for x in range(size) for y in range(size) if grid[x][y] == PointType.DEFAULT.value]
    start = choice(free)
    end = start
    while end == start:
        end = choice(free)

    grid[start[0]][start[1]] = PointType.CENTER.value
    grid[end[0]][end[1]] = PointType.END.value

    candidates = [(x, y) for x in range(size) for y in range(size)
                  if grid[x][y] == 0 and (x, y) not in (start, end)]

    wall_target = int(len(candidates) * (fullness / 300))

    shuffle(candidates)
    added = 0
    for x, y in candidates:
        original = grid[x][y]
        grid[x][y] = 1
        if is_connected(grid, start, end, size):
            added += 1
            if added >= wall_target:
                break
        else:
            grid[x][y] = original
    return grid
