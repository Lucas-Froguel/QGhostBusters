from numpy import random
from pygame import Vector2


def generate_random_positions(
    worldSize: Vector2 = None, player_position: Vector2 = None
):
    default_x, default_y = 5, 2
    if player_position is not None:
        default_x = max(default_x, player_position.x + 5)
    x = random.randint(default_x, worldSize.x)
    y = random.randint(default_y, worldSize.y - 2)

    return Vector2(x, y)
