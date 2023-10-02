from typing import Optional

import numpy as np
from pygame import Vector2
from qutip import Qobj, ket, destroy, tensor, qeye

from src.Units.splitter import SplitterType
from src.settings import ATTACK_RADIUS, MAX_GHOSTS_PER_STATE


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


a = destroy(MAX_GHOSTS_PER_STATE)
BS = (1j * np.pi / 4 * (tensor(a, a.dag()) + tensor(a.dag(), a))).expm()


def beam_splitter(
    quantum_state: Qobj,
    affected_ghost_index: int,
    other_state_index: Optional[int] = None,
) -> Qobj:
    """
    Perform beam-splitter operation.

    :param quantum_state: one of the two input states
    :param affected_ghost_index: there may be several systems in the state, choose this one
    :param other_state_index: index of the otehr state, if two existing ghosts interact. If not given, vacuum.
    """
    dim = max(quantum_state.shape)
    n_systems = len(quantum_state.dims[0])
    if dim > 1000:
        raise NotImplementedError("The size of the matrix is too large")

    add_ghost = False
    if other_state_index is None:
        other_state = ket([0], MAX_GHOSTS_PER_STATE)
        quantum_state = tensor(quantum_state, other_state)
        other_state_index = -1
        add_ghost = True

    expanded_BS = BS

    if n_systems > 1:
        index_order = list(range(n_systems + add_ghost))
        index_order[affected_ghost_index], index_order[n_systems - 2 + add_ghost] = (
            index_order[n_systems - 2 + add_ghost],
            index_order[affected_ghost_index],
        )
        index_order[other_state_index], index_order[n_systems - 1 + add_ghost] = (
            index_order[n_systems - 1 + add_ghost],
            index_order[other_state_index],
        )

        ghosts = [MAX_GHOSTS_PER_STATE] * int(n_systems - 2 + add_ghost)

        expanded_BS = tensor(qeye(ghosts if ghosts else [0]), BS).permute(index_order)

    try:
        final_state = expanded_BS * quantum_state
    except Exception:
        final_state = BS * quantum_state

    return final_state
