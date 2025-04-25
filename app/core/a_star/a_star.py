import heapq
from app.utils.config import config
from app.models.point_type import PointType


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    open_set, history, came_from = [], [], {}
    g_score, f_score = {start: 0}, {start: heuristic(start, end)}
    heapq.heappush(open_set, (0, start))
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, history
        for dx, dy in config.a_star.DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            if grid[neighbor[0]][neighbor[1]] == PointType.WALL.value:
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
            if cell == PointType.CENTER.value:
                start = (row_idx, col_idx)
            elif cell == PointType.END.value:
                end = (row_idx, col_idx)
    return a_star(pixels, start, end)
