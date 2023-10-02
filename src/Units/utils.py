import numpy as np
from pygame import Vector2

from src.Units.splitter import SplitterType
from src.settings import ATTACK_RADIUS


def is_ghost_in_players_radius(player_pos: Vector2, ghost_pos: Vector2) -> bool:
    """
    Check whether the ghost is inside player's radius.
    """
    return (player_pos - ghost_pos).length_squared() <= ATTACK_RADIUS**2


def two_ghost_coming_from_different_size_of_splitter(
    g1, g2, splitterType: SplitterType
) -> bool:
    return (
        g1 != g2  # not the same ghost
        and np.allclose(g1.position, g2.position, 1e-2)  # same position
        and g1.turn == g2.turn  # at the same turn (we did update on one of them)
        and (
            splitterType == "45"
            and sum(g1.last_move) + sum(g2.last_move)
            in [Vector2(-1, 1), Vector2(1, -1)]
            or splitterType == "125"
            and sum(g1.last_move) + sum(g2.last_move)
            in [Vector2(-1, -1), Vector2(1, 1)]
        )
    )
