import os
from typing import Optional

import numpy as np
from pygame import Vector2, Surface
from pygame.image import load
from pygame.transform import scale
from qutip import Qobj, ket, destroy, tensor, qeye

from src.settings import MAX_GHOSTS_PER_STATE


def is_in_given_radius(position_1: Vector2, position_2: Vector2, radius: float) -> bool:
    """
    Check whether the ghost is inside player's radius.
    """
    return (position_1 - position_2).length() <= radius


def two_ghost_coming_from_different_sides_of_splitter(g1, g2, splitterType) -> bool:
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
    vector_length = max(quantum_state.shape)
    n_systems = len(quantum_state.dims[0])
    if vector_length > 2000:
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

        dims = [MAX_GHOSTS_PER_STATE] * int(n_systems - 2 + add_ghost)

        expanded_BS = tensor(qeye(dims if dims else [0]), BS).permute(index_order)

    try:
        final_state = expanded_BS * quantum_state
    except Exception:
        final_state = BS * quantum_state

    return final_state


def find_tensored_components(idx: int, n_comp: int) -> list[int]:
    """ "
    Returns array of size n_comp that corresponds to the quantum state of the ghost
    as |i_0, i_1, ..., i_n>
    """
    res = []
    n = n_comp - 1
    while idx > 0:
        this_power = MAX_GHOSTS_PER_STATE**n
        this_component = idx // this_power
        idx -= this_power * this_component
        res.append(this_component)
        n -= 1
    return np.array(res + [0] * (n_comp - len(res)))


def load_all_images_in_folder(
    folder_path: str = None, file_name: str = None, cellSize: Vector2 = None
) -> [Surface]:
    num_files = len(os.listdir(folder_path))
    image_files = [f"{file_name}{i}.png" for i in range(num_files)]

    if cellSize:
        images = [
            scale(load(os.path.join(folder_path, filename)), cellSize)
            for filename in image_files
        ]
    else:
        images = [load(os.path.join(folder_path, filename)) for filename in image_files]

    return images
