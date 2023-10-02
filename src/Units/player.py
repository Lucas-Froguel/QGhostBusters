
import numpy as np
import math
from pygame import Vector2
from pygame.image import load
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from qutip import qeye, ket, tensor

from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_ghost_in_players_radius
from src.settings import MAX_GHOSTS_PER_STATE
from pygame.transform import rotate
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_ghost_in_players_radius


class Player(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        self.image = load("src/Units/sprites/player.png")
        self.image = scale(self.image, self.cellSize)
        self.direction: Vector2 = Vector2(1, 0)

    def measure(self, ghosts_group: list[QGhost], visible_ghosts_group: RenderUpdates):
        """
        Check whether we are in the zone of application of user's weapon.
        If so, decrease the number of ghosts.

        :param ghosts_group: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        for qghost in ghosts_group:
            n_ghosts = len(qghost.visible_parts)
            if n_ghosts == 1:
                continue
            indices_to_remove = []
            for i, ghost in enumerate(qghost.visible_parts):
                if is_ghost_in_players_radius(self.position, ghost.position):
                    # <n|psi>
                    possible_vectors = [
                        tensor(
                            [
                                ket([n], MAX_GHOSTS_PER_STATE).dag()
                                if g == i
                                else qeye(MAX_GHOSTS_PER_STATE)
                                for g in range(n_ghosts)
                            ]
                        )
                        * qghost.quantum_state
                        for n in range(MAX_GHOSTS_PER_STATE)
                    ]
                    norms = [v.norm() for v in possible_vectors]
                    n_in_state = np.random.choice(
                        list(range(MAX_GHOSTS_PER_STATE)),
                        p=np.array(norms) / np.sum(norms),
                    )

                    qghost.quantum_state = possible_vectors[n_in_state].unit()
                    if n_in_state == 0:
                        indices_to_remove.append(i)
                    else:
                        # probability of |0> in j-th Hilbert space
                        zero_vectors = np.array(
                            [
                                (
                                    tensor(
                                        [
                                            ket([0], MAX_GHOSTS_PER_STATE).dag()
                                            if g != j
                                            else qeye(MAX_GHOSTS_PER_STATE)
                                            for g in range(n_ghosts - 1)
                                        ]
                                    )
                                    * qghost.quantum_state
                                ).norm()
                                for j in range(n_ghosts)
                                if j != i
                            ]
                        )
                        indices_to_remove.append(np.argmin(np.abs(1 - zero_vectors)))
                    break

            for i in indices_to_remove:
                visible_ghosts_group.remove(qghost.visible_parts.pop(i))
            if not qghost.visible_parts:
                ghosts_group.remove(qghost)

    def move(self, moveVector: Vector2) -> None:
        super().move(moveVector=moveVector)

        angle = math.acos(self.direction.dot(moveVector) / (self.direction.length() * moveVector.length()))
        self.direction = moveVector
        self.image = rotate(self.image, -math.degrees(angle))

