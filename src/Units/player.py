
import time

import numpy as np
import math
from pytmx import TiledMap
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.transform import scale

from src.SoundEffects.sound_manager import PlayerSoundManager
from src.Units.splitter import GhostSplitter
from src.settings import PLAYER_MEASURE_RADIUS, PLAYER_INITIAL_HEALTH, PLAYER_MEASURE_TIME
from pygame.transform import rotate
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.weapon import Weapon


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
        self.max_health = PLAYER_INITIAL_HEALTH
        self.health = PLAYER_INITIAL_HEALTH
        self.min_measure_time = PLAYER_MEASURE_TIME
        self.last_measure_time: int = 0
        self.ready_to_measure: bool = True

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

    def measure(self, qghosts: list[QGhost]):
        """
        Check whether we are in the zone of application of user's measurement apparatus.
        If so, collapse the ghosts to one spot.

        :param ghosts_group: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        if self.ready_to_measure:
            for qghost in qghosts:
                if qghost.collapse_wave_function(player=self):
                    self.sound_manager.play_measure_sound()
                    self.last_measure_time = int(time.time())
                    self.ready_to_measure = False
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

    def check_measure_time(self):
        check_if_able_to_measure = int(time.time() - self.last_measure_time) > self.min_measure_time
        if not self.ready_to_measure and check_if_able_to_measure:
            self.sound_manager.play_ready_to_measure_sound()
            self.ready_to_measure = True
    
    def update(self, moveVector: Vector2 = None) -> None:
        super().update(moveVector=moveVector)
        if self.collides_with_wall():
            self.move(moveVector=-moveVector, does_rotate=False)

        self.check_measure_time()

        self.weapon.update()
