from pygame import Vector2
from src.settings import ATTACK_RADIUS


def is_ghost_in_players_radius(player_pos: Vector2, ghost_pos: Vector2) -> bool:
    """
    Check whether the ghost is inside player's radius.
    """
    return (player_pos - ghost_pos).length_squared() <= ATTACK_RADIUS**2
