import random
from itertools import permutations
import numpy as np
from copy import deepcopy

def create_random_ant_grid(size: int, fullness):
    start = random.randint(0, size - 1), random.randint(0, size - 1)
    end = start

    wall_chance = fullness / 100

    while end == start:
        end = random.randint(0, size - 1), random.randint(0, size - 1)

    grid = [[random.choices([0, 1], weights=[1 - wall_chance, wall_chance])[0]
             for _ in range(size)] for _ in range(size)]

    return grid

EVAPORATION = 0.5
Q = 100

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1

def find_colony_and_foods(grid):
    colony = None
    foods = []
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 3:
                colony = (i, j)
            elif val == 2:
                foods.append((i, j))
    return colony, foods

def heuristic(a, b):
    return 1 / (abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1)

def ant_algorithm(grid, num_ants=50, iterations=100):
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

        pheromone *= (1 - EVAPORATION)

        for path, score in paths:
            if not path: continue
            pheromone_value = Q / (score + 1)
            for idx in range(1, len(path)):
                x1, y1 = path[idx - 1]
                x2, y2 = path[idx]
                dir_idx = DIRS.index((x2 - x1, y2 - y1))
                pheromone[x1][y1][dir_idx] += pheromone_value

    return best_path

def simulate_ant(grid, pheromone, start, food_sources):
    best_total_path = []
    best_total_len = float('inf')

    for perm in permutations(food_sources):
        sequence = [start] + list(perm)
        total_path = []
        total_len = 0
        failed = False
        for i in range(len(sequence) - 1):
            p1, p2 = sequence[i], sequence[i+1]
            subpath = bfs_path(grid, pheromone, p1, p2)
            if not subpath:
                failed = True
                break
            if total_path and subpath[0] == total_path[-1]:
                subpath = subpath[1:]
            total_path += subpath
            total_len += len(subpath)
        if not failed and total_len < best_total_len:
            best_total_len = total_len
            best_total_path = total_path
            best_sequence = sequence

    return best_total_path, best_total_len

def bfs_path(grid, pheromone, start, goal):
    from heapq import heappush, heappop
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
        for idx, (dx, dy) in enumerate(DIRS):
            nx, ny = x + dx, y + dy
            if is_valid(grid, nx, ny):
                pher = pheromone[x][y][idx]
                heur = heuristic((nx, ny), goal)
                heappush(heap, (cost + 1 / (pher + 1e-9) + 1 / (heur + 1e-9), (nx, ny), path))
    return []

def find_path_ant(pixels: list[list[int]]):
    grid = deepcopy(pixels)
    path = ant_algorithm(grid)
    history = path.copy() if path else []
    return path, history