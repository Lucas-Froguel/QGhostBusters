import numpy as np
from pygame import Vector2

from src.Units.splitter import SplitterType
from src.settings import ATTACK_RADIUS


def is_ghost_in_players_radius(player_pos: Vector2, ghost_pos: Vector2) -> bool:
    """
    Check whether the ghost is inside player's radius.
    """
    return (player_pos - ghost_pos).length_squared() <= ATTACK_RADIUS**2


def two_ghost_coming_from_different_sides_of_splitter(
    g1, g2, splitterType: SplitterType
) -> bool:
    if g1 != g2 and np.allclose(  # not the same ghost
        g1.position, g2.position, 3e-2
    ):  # same position
        last_move_sum = g1.last_move + g2.last_move
        if (
            splitterType == "45"
            and last_move_sum.x == -last_move_sum.y
            or splitterType == "125"
            and last_move_sum.x == last_move_sum.y
        ):
            return True
    return False
