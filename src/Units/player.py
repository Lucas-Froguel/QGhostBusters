import numpy as np
import math
from pytmx import TiledMap
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from qutip import ket

from src.SoundEffects.sound_manager import PlayerSoundManager
from src.Units.splitter import GhostSplitter
from src.Units.weapon import Weapon
from src.settings import MAX_GHOSTS_PER_STATE, PLAYER_MEASURE_RADIUS, INITIAL_HEALTH
from pygame.transform import rotate
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_in_given_radius, find_tensored_components
from src.Units.trap import Trap



class Player(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
        map_data: TiledMap = None,
        splitters: [GhostSplitter] = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        self.image = load("src/Units/sprites/enemy1.png")
        self.image = scale(self.image, self.cellSize)
        self.direction: Vector2 = Vector2(1, 0)
        self.sound_manager = PlayerSoundManager(channel=self.channel)
        self.measure_radius = PLAYER_MEASURE_RADIUS
        self.health = INITIAL_HEALTH
        self.map_data = map_data
        self.splitters = splitters
        self.weapon = Weapon(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=self.position,
            channel=self.channel,
            map_data=self.map_data,
        )

    def attack(self):
        self.weapon.attack(direction=self.direction, position=self.position)
        self.sound_manager.play_attack_sound()

    def measure(self, ghosts_group: list[QGhost], visible_ghosts_group: RenderUpdates):
        """
        Check whether we are in the zone of application of user's measurement apparatus.
        If so, collapse the ghosts to one spot.

        :param ghosts_group: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        for qghost in ghosts_group:
            n_ghosts = len(qghost.visible_parts)
            if n_ghosts == 1:
                continue
            for i, ghost in enumerate(qghost.visible_parts):
                if is_in_given_radius(
                    self.position, ghost.position, PLAYER_MEASURE_RADIUS
                ):
                    probs = np.abs(qghost.quantum_state.full()[:, 0]) ** 2
                    # choose one vector to survive based on its probability
                    surviving_state_idx = np.random.choice(
                        list(range(MAX_GHOSTS_PER_STATE**n_ghosts)),
                        p=probs / np.sum(probs),
                    )
                    numbers_of_ghosts_here = find_tensored_components(
                        surviving_state_idx, n_ghosts
                    )
                    qghost.quantum_state = ket(
                        numbers_of_ghosts_here[numbers_of_ghosts_here > 0],
                        MAX_GHOSTS_PER_STATE,
                    )
                    surviving_state_indices = set(
                        np.where(numbers_of_ghosts_here > 0)[0]
                    )
                    self.sound_manager.play_attack_sound()
                    for k in range(n_ghosts - 1, -1, -1):
                        if k not in surviving_state_indices:
                            visible_ghosts_group.remove(qghost.visible_parts.pop(k))
                    break

    def move(self, moveVector: Vector2, does_rotate: bool = True) -> None:
        super().move(moveVector=moveVector)

        if does_rotate:
            angle = math.acos(
                self.direction.dot(moveVector)
                / (self.direction.length() * moveVector.length())
            )
            self.direction = moveVector
            self.image = rotate(self.image, -math.degrees(angle))

    def collides_with_wall(self):
        walls = self.map_data.layernames["Walls"].tiles()
        for x, y, _ in walls:
            if np.allclose(self.position, Vector2(x, y)):
                return True
        for splitter in self.splitters:
            if np.allclose(self.position, splitter.position):
                return True
        return False

    def update(self, moveVector: Vector2 = None) -> None:
        super().update(moveVector=moveVector)
        if self.collides_with_wall():
            self.move(moveVector=-moveVector, does_rotate=False)
