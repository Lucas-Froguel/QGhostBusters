import numpy as np
import math
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates
from pygame.transform import scale, rotate
from qutip import qeye, ket, tensor

from src.settings import MAX_GHOSTS_PER_STATE
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_ghost_in_players_radius
from src.SoundEffects.sound_manager import PlayerSoundManager


class Player(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position, channel=channel)
        self.image = load("src/Units/sprites/enemy1.png")
        self.image = scale(self.image, self.cellSize)
        self.direction: Vector2 = Vector2(1, 0)
        self.sound_manager = PlayerSoundManager(channel=self.channel)

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
            for i, ghost in enumerate(qghost.visible_parts):
                if is_ghost_in_players_radius(self.position, ghost.position):
                    # projections on |0> for each ghost
                    possible_vectors = [
                        tensor(
                            [
                                ket([0], MAX_GHOSTS_PER_STATE).dag()
                                if g == j
                                else qeye(MAX_GHOSTS_PER_STATE)
                                for g in range(n_ghosts)
                            ]
                        )
                        * qghost.quantum_state
                        for j in range(n_ghosts)
                    ]
                    # norms of each vector, proportional to probability to measure |n>, n>0 in that state
                    # max is to trim floating point errors
                    norms = [max(0, 1 - v.norm()) for v in possible_vectors]
                    # choose one vector to survive based on probability (1 - P(|0>)) of non-zero state
                    surviving_state_idx = np.random.choice(
                        list(range(n_ghosts)),
                        p=np.array(norms) / np.sum(norms),
                    )

                    qghost.quantum_state = possible_vectors[surviving_state_idx].unit()
                    break

            for i in indices_to_remove:
                self.sound_manager.play_measure_sound()
                visible_ghosts_group.remove(qghost.visible_parts.pop(i))

            if not qghost.visible_parts:
                ghosts_group.remove(qghost)

    def move(self, moveVector: Vector2) -> None:
        super().move(moveVector=moveVector)

        angle = math.acos(
            self.direction.dot(moveVector)
            / (self.direction.length() * moveVector.length())
        )
        self.direction = moveVector
        self.image = rotate(self.image, -math.degrees(angle))
