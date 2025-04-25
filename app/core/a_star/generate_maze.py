from heapq import heappush, heappop
from random import choice, randrange, random, shuffle
from collections import deque
from app.models.point_type import PointType
from app.models.point import Point
from app.utils.config import config


def in_bounds(x, y, size):
    return 0 <= x < size and 0 <= y < size


def is_connected(grid, start, end, size):
    visited = [[False] * size for _ in range(size)]
    q = deque([start])
    visited[start.x][start.y] = True
    while q:
        p = q.popleft()
        if p == end:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = p.x + dx, p.y + dy
            if in_bounds(nx, ny, size) and not visited[nx][ny] and grid[nx][ny] in (0, 3):
                visited[nx][ny] = True
                q.append(Point(nx, ny))
    return False


def generate_maze(size: int, fullness):
    grid = [[PointType.WALL.value for _ in range(size)] for _ in range(size)]
    start = Point(randrange(1, size, 2), randrange(1, size, 2))
    grid[start.x][start.y] = PointType.DEFAULT.value
    walls = []
    for dx, dy in config.a_star.MAZE_DIRECTIONS:
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
        for dx, dy in config.a_star.MAZE_DIRECTIONS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, size) and grid[nx][ny] == 1:
                heappush(walls, (random(), Point(x, y), Point(nx, ny)))
    free = [Point(x, y) for x in range(size)
            for y in range(size) if grid[x][y] == PointType.DEFAULT.value]
    end = start = choice(free)
    while end == start:
        end = choice(free)
    grid[start.x][start.y] = PointType.CENTER.value
    grid[end.x][end.y] = PointType.END.value
    candidates = [Point(x, y) for x in range(size) for y in range(size)
                  if grid[x][y] == PointType.DEFAULT.value and Point(x, y) not in (start, end)]
    wall_target = int(len(candidates) * (fullness / 300))
    shuffle(candidates)
    added = 0
    for p in candidates:
        original = grid[p.x][p.y]
        grid[p.x][p.y] = PointType.WALL.value
        if is_connected(grid, start, end, size):
            added += 1
            if added >= wall_target:
                break
        else:
            grid[p.x][p.y] = original
    return grid
