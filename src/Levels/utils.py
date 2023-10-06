
from numpy import random
from pygame import Vector2


def generate_random_positions(worldSize: Vector2 = None):
    x = random.randint(5, worldSize.x)
    y = random.randint(2, worldSize.y - 2)

    return Vector2(x, y)
