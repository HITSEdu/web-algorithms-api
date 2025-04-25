from heapq import heappush, heappop
from copy import deepcopy
import numpy as np
from app.utils.config import config
from app.models.point_type import PointType


def is_valid(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != PointType.WALL.value


def heuristic(a, b):
    return 1 / (abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1)


def find_colony_and_foods(grid):
    colony = None
    foods = []
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == PointType.END.value:
                colony = (i, j)
            elif val == PointType.CENTER.value:
                foods.append((i, j))
    return colony, foods


def ant_algorithm(grid, num_ants, iterations):
    colony, food_sources = find_colony_and_foods(grid)
    if not colony or not food_sources:
        return []
    n, m = len(grid), len(grid[0])
    pheromone = np.ones((n, m, 4))
    best_path = []
    best_score = float('inf')
    for _ in range(iterations):
        paths = []
        for _ in range(num_ants):
            path, score = simulate_ant(grid, pheromone, colony, food_sources)
            paths.append((path, score))
            if score < best_score:
                best_score = score
                best_path = path
        pheromone *= (1 - config.ant_colony.EVAPORATION)
        for path, score in paths:
            if not path:
                continue
            pheromone_value = config.ant_colony.Q / (score + 1)
            for idx in range(1, len(path)):
                x1, y1 = path[idx - 1]
                x2, y2 = path[idx]
                dir_idx = config.ant_colony.DIRECTIONS.index((x2 - x1, y2 - y1))
                pheromone[x1][y1][dir_idx] += pheromone_value
    return best_path


def simulate_ant(grid, pheromone, start, food_sources):
    unvisited = set(food_sources)
    current = start
    path = []
    total_len = 0
    while unvisited:
        next_point = min(unvisited, key=lambda p: abs(current[0] - p[0]) + abs(current[1] - p[1]))
        subpath = bfs_path(grid, pheromone, current, next_point)
        if not subpath:
            return [], float('inf')
        if path and subpath[0] == path[-1]:
            subpath = subpath[1:]
        path.extend(subpath)
        total_len += len(subpath)
        current = next_point
        unvisited.remove(next_point)
    subpath = bfs_path(grid, pheromone, current, start)
    if not subpath:
        return [], float('inf')
    if path and subpath[0] == path[-1]:
        subpath = subpath[1:]
    path.extend(subpath)
    total_len += len(subpath)
    return path, total_len


def bfs_path(grid, pheromone, start, goal):
    visited = set()
    heap = [(0, start, [])]
    while heap:
        cost, current, path = heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == goal:
            return path
        x, y = current
        for idx, (dx, dy) in enumerate(config.ant_colony.DIRECTIONS):
            nx, ny = x + dx, y + dy
            if is_valid(grid, nx, ny):
                pher = pheromone[x][y][idx]
                heur = heuristic((nx, ny), goal)
                heappush(heap, (cost + 1 / (pher + 1e-9) + 1 / (heur + 1e-9), (nx, ny), path))
    return []


def find_path_ant(pixels: list[list[int]]):
    grid = deepcopy(pixels)
    path = ant_algorithm(grid, config.ant_colony.NUM_ANTS, config.ant_colony.EPS)
    history = path.copy() if path else []
    return path, history
