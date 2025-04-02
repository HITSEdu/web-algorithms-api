import heapq
import random


def create_random(size: int, fullness):
    start = random.randint(0, size - 1), random.randint(0, size - 1)
    end = start

    wall_chance = fullness / 100

    while end == start:
        end = random.randint(0, size - 1), random.randint(0, size - 1)

    grid = [[random.choices([0, 1], weights=[1 - wall_chance, wall_chance])[0] for _ in range(size)] for _ in
            range(size)]

    grid[start[0]][start[1]] = 2
    grid[end[0]][end[1]] = 3

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
