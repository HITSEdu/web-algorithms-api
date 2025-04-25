import math
import random
from typing import List
from app.models.point import Point
from app.utils.config import config


def calculate_distance(p1: Point, p2: Point) -> float:
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def total_path_distance(path: List[int], pts: List[Point]) -> float:
    path_len = len(path)
    return sum(calculate_distance(pts[path[i]], pts[path[(i + 1) % path_len]])
                for i in range(path_len))


def crossover(parent1: List[int], parent2: List[int]) -> List[int]:
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = parent1[start:end]
    child += [gene for gene in parent2 if gene not in child]
    return child


def mutate(path: List[int]) -> List[int]:
    path_len = len(path)
    for i in range(path_len):
        if random.random() < config.genetic.MUTATION_RATE:
            j = random.randint(0, path_len - 1)
            path[i], path[j] = path[j], path[i]
    return path


def solve_tsp_genetic(points: List[Point]) -> dict[str, List]:
    num_points = len(points)
    if num_points < 2:
        return {"path": [], "history": []}
    history_interval = max(1, config.genetic.GENERATIONS // 20)
    population = [random.sample(range(num_points), num_points)
                  for _ in range(config.genetic.POPULATION_SIZE)]
    history = []
    best_distance = float('inf')
    for generation in range(config.genetic.GENERATIONS):
        population.sort(key=lambda path: total_path_distance(path, points))
        current_best = population[0]
        current_dist = total_path_distance(current_best, points)
        if (generation % history_interval == 0 or current_dist < best_distance * 0.99):
            path_ids = [points[i].id for i in current_best]
            if not history or path_ids != history[-1]:
                history.append(path_ids)
                best_distance = current_dist
        next_gen = population[:config.genetic.ELITE_SIZE]
        while len(next_gen) < config.genetic.POPULATION_SIZE:
            candidates = random.sample(population[:50], 2)
            parent1, parent2 = sorted(candidates, key=lambda p: total_path_distance(p, points))
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_gen.append(child)
        population = next_gen
    best_path = min(population, key=lambda p: total_path_distance(p, points))
    final_path = [points[i].id for i in best_path]
    if not history or final_path != history[-1]:
        history.append(final_path)
    return {
        "path": final_path,
        "history": history
    }
