import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from qutip import projection, qeye, num, ket, bra, tensor

from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_ghost_in_players_radius
from src.settings import MAX_GHOSTS_PER_STATE


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

    def attack(self, ghosts_group: list[QGhost], visible_ghosts_group: RenderUpdates):
        """
        Check whether we are in the zone of application of user's weapon.
        If so, decrease the number of ghosts.

        :param ghosts_group: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        for qghost in ghosts_group:
            n_ghosts = len(qghost.visible_parts)
            print(len(ghosts_group), n_ghosts, qghost.quantum_state.norm())
            indices_to_remove = []
            for i in range(n_ghosts):
                ghost = qghost.visible_parts[i]
                if is_ghost_in_players_radius(self.position, ghost.position):
                    projector_1 = sum(
                        [
                            tensor(
                                [qeye(MAX_GHOSTS_PER_STATE) if g != i else ket([n], MAX_GHOSTS_PER_STATE).dag()
                                for g in range(n_ghosts)]
                            )
                            for n in range(1, MAX_GHOSTS_PER_STATE)
                        ]
                    )
                    projector_0 = tensor(
                                [qeye(MAX_GHOSTS_PER_STATE) if g != i else ket([0], MAX_GHOSTS_PER_STATE).dag()
                                for g in range(n_ghosts)]
                            )
                    quantum_state_0 = projector_0 * qghost.quantum_state
                    quantum_state_1 = projector_1 * qghost.quantum_state
                    if np.random.rand() > quantum_state_1.norm():
                        qghost.quantum_state = quantum_state_1.unit()
                    else:
                        qghost.quantum_state = quantum_state_0.unit()
                    visible_ghosts_group.remove(qghost.visible_parts.pop(i))
            if not qghost.visible_parts:
                ghosts_group.remove(qghost)
