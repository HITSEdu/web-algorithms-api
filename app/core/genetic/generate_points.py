from typing import List
from random import randint
from app.models.point import Point
from app.utils.config import config


def generate_random_points(
    count: int, width: int = config.genetic.DEFAULT_WIDTH, height: int = config.genetic.DEFAULT_HEIGHT) -> List[Point]:
    positions = [
        Point(_id=i, x=randint(config.genetic.MARGIN, width - config.genetic.MARGIN),
              y=randint(config.genetic.MARGIN, height - config.genetic.MARGIN))
        for i in range(count)]
    return positions
