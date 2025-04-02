from random import randint, choices

def generate(size: int, fullness):
    start = randint(0, size - 1), randint(0, size - 1)
    end = start

    wall_chance = fullness / 100

    while end == start:
        end = randint(0, size - 1), randint(0, size - 1)

    grid = [[choices([0, 1], weights=[1 - wall_chance, wall_chance])[0] for _ in range(size)] for _ in range(size)]

    return grid