import heapq
import random
from collections import deque


def create_random(size: int, fullness):
    grid = [[1 for _ in range(size)] for _ in range(size)]

    def in_bounds(x, y):
        return 0 <= x < size and 0 <= y < size

    DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    start = (random.randrange(1, size, 2), random.randrange(1, size, 2))
    grid[start[0]][start[1]] = 0
    walls = []

    for dx, dy in DIRS:
        nx, ny = start[0] + dx, start[1] + dy
        if in_bounds(nx, ny):
            heapq.heappush(walls, (random.random(), start, (nx, ny)))

    while walls:
        _, from_cell, to_cell = heapq.heappop(walls)
        x, y = to_cell
        if not in_bounds(x, y) or grid[x][y] == 0:
            continue

        wall_x = (from_cell[0] + x) // 2
        wall_y = (from_cell[1] + y) // 2

        grid[wall_x][wall_y] = 0
        grid[x][y] = 0

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and grid[nx][ny] == 1:
                heapq.heappush(walls, (random.random(), (x, y), (nx, ny)))

    free = [(x, y) for x in range(size) for y in range(size) if grid[x][y] == 0]
    start = random.choice(free)
    end = start
    while end == start:
        end = random.choice(free)

    grid[start[0]][start[1]] = 2
    grid[end[0]][end[1]] = 3

    def is_connected(grid, start, end):
        visited = [[False] * size for _ in range(size)]
        q = deque([start])
        visited[start[0]][start[1]] = True
        while q:
            x, y = q.popleft()
            if (x, y) == end:
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny) and not visited[nx][ny] and grid[nx][ny] in (0, 3):
                    visited[nx][ny] = True
                    q.append((nx, ny))
        return False

    candidates = [(x, y) for x in range(size) for y in range(size)
                  if grid[x][y] == 0 and (x, y) not in (start, end)]

    wall_target = int(len(candidates) * (fullness / 300))

    random.shuffle(candidates)
    added = 0
    for x, y in candidates:
        original = grid[x][y]
        grid[x][y] = 1
        if is_connected(grid, start, end):
            added += 1
            if added >= wall_target:
                break
        else:
            grid[x][y] = original

    return grid


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b

    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    history = []

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print(path)
            return path, history

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)

            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue

            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                history.append(neighbor)

    return [], history


def find_path(pixels):
    start, end = None, None

    for row_idx, row in enumerate(pixels):
        for col_idx, cell in enumerate(row):
            if cell == 2:
                start = (row_idx, col_idx)
            elif cell == 3:
                end = (row_idx, col_idx)

    return a_star(pixels, start, end)
