import math
import random

from pydantic import BaseModel
from typing import List

class Point(BaseModel):
    id: int
    x: float
    y: float

class Canvas(BaseModel):
    points: List[Point]


def generate_random_points(count: int, width: int = 500, height: int = 350) -> List[Point]:
    margin = 40
    return [
        Point(
            id=i,
            x=random.randint(margin, width - margin),
            y=random.randint(margin, height - margin)
        )
        for i in range(count)
    ]


def solve_tsp_genetic(points: List[Point]) -> dict[str, List]:

    def distance(p1: Point, p2: Point) -> float:
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def total_path_distance(path: List[int], pts: List[Point]) -> float:
        return sum(distance(pts[path[i]], pts[path[(i + 1) % len(path)]])
                   for i in range(len(path)))

    def crossover(parent1: List[int], parent2: List[int]) -> List[int]:
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = parent1[start:end]

        child += [gene for gene in parent2 if gene not in child]
        return child

    def mutate(path: List[int], mutation_rate: float = 0.02) -> List[int]:
        for i in range(len(path)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(path) - 1)
                path[i], path[j] = path[j], path[i]
        return path

    num_points = len(points)
    if num_points < 2:
        return {"path": [], "history": []}

    population_size = 100
    generations = 500
    elite_size = 10
    history_interval = max(1, generations // 20)
    mutation_rate = 0.02

    population = [random.sample(range(num_points), num_points)
                  for _ in range(population_size)]
    history = []
    best_distance = float('inf')

    for generation in range(generations):
        population.sort(key=lambda path: total_path_distance(path, points))
        current_best = population[0]
        current_dist = total_path_distance(current_best, points)

        if (generation % history_interval == 0 or
                current_dist < best_distance * 0.99):

            path_ids = [points[i].id for i in current_best]

            if not history or path_ids != history[-1]:
                history.append(path_ids)
                best_distance = current_dist

        next_gen = population[:elite_size]

        while len(next_gen) < population_size:
            candidates = random.sample(population[:50], 2)
            parent1, parent2 = sorted(candidates,
                                      key=lambda p: total_path_distance(p, points))

            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
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