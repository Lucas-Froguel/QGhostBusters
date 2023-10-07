import time
import math
import numpy as np

from pytmx import TiledMap
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.transform import scale

from src.SoundEffects.sound_manager import PlayerSoundManager
from src.Units.splitter import GhostSplitter
from src.Units.trap import Trap
from src.Units.weapon import Weapon
from src.settings import (
    PLAYER_MEASURE_RADIUS,
    PLAYER_INITIAL_HEALTH,
    PLAYER_MEASURE_TIME,
)
from pygame.transform import rotate
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost


class Player(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
        map_data: TiledMap = None,
        does_map_have_tile_dont_pass: bool = None,
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
        # visual variables
        self.image = load("src/Units/sprites/character.png")
        self.image = scale(self.image, self.cellSize)
        self.direction: Vector2 = Vector2(1, 0)
        self.sound_manager = PlayerSoundManager(channel=self.channel)

        # gameplay variables
        self.measure_radius = PLAYER_MEASURE_RADIUS
        self.max_health = PLAYER_INITIAL_HEALTH
        self.health = PLAYER_INITIAL_HEALTH
        self.min_measure_time = PLAYER_MEASURE_TIME
        self.last_measure_time: int = 0
        self.ready_to_measure: bool = True

        # score variables
        self.num_of_fallen_traps: int = 0
        self.qghosts_killed: int = 0
        self.visible_ghosts_killed: int = 0

        # functionality variables
        self.map_data = map_data
        self.does_map_have_tile_dont_pass = does_map_have_tile_dont_pass
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

        :param qghosts: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        if self.ready_to_measure:
            for qghost in qghosts:
                if qghost.collapse_wave_function(player=self):
                    self.sound_manager.play_measure_sound()
                    self.last_measure_time = int(time.time())
                    self.ready_to_measure = False
                    self.weapon.measurer.measure(position=self.position)
                    break

    def move(self, moveVector: Vector2, does_rotate: bool = True) -> None:
        super().move(moveVector=moveVector)

        if does_rotate:
            angle = moveVector.angle_to(self.direction)
            self.direction = moveVector
            self.image = rotate(self.image, angle)

    def collides_with_wall(self):
        walls = self.map_data.layernames["Walls"].tiles()
        for x, y, _ in walls:
            if np.allclose(self.position, Vector2(x, y)):
                return True
        for splitter in self.splitters:
            if np.allclose(self.position, splitter.position):
                return True
        return False

    def collides_with_splitter(self):
        for splitter in self.splitters:
            if np.allclose(self.position, splitter.position):
                return True
        return False

    def collides_with_non_walkable_floor(self):
        if not self.does_map_have_tile_dont_pass:
            return False
        floors = self.map_data.layernames["TileDontPass"].tiles()
        for x, y, _ in floors:
            if np.allclose(self.position, Vector2(x, y)):
                return True
        return False

    def collides_with_anything(self):
        check_collision_functions = [
            self.collides_with_splitter,
            self.collides_with_wall,
            self.collides_with_non_walkable_floor,
        ]
        for collision_function in check_collision_functions:
            if collision_function():
                return True
        return False

    def check_measure_time(self):
        check_if_able_to_measure = (
            int(time.time() - self.last_measure_time) > self.min_measure_time
        )
        if not self.ready_to_measure and check_if_able_to_measure:
            self.sound_manager.play_ready_to_measure_sound()
            self.ready_to_measure = True

    def control_commands(
        self,
        measureCommand: bool = None,
        attackCommand: bool = None,
        ghosts_group=None,
        shots_group=None,
    ):
        if measureCommand:
            self.measure(ghosts_group)  # wave func collapse
        elif attackCommand:
            self.attack()
            shots_group.add(self.weapon.shots)
        shots_group.remove(*self.weapon.dead_shots)

    def update(
        self,
        moveVector: Vector2 = None,
        measureCommand: bool = None,
        attackCommand: bool = None,
        ghosts_group=None,
        shots_group=None,
        traps=None,
    ) -> None:
        super().update(moveVector=moveVector)

        if self.collides_with_anything():
            self.move(moveVector=-moveVector, does_rotate=False)
        self.check_if_on_trap(traps)
        self.check_measure_time()
        self.weapon.update()

        self.control_commands(
            measureCommand=measureCommand,
            attackCommand=attackCommand,
            ghosts_group=ghosts_group,
            shots_group=shots_group,
        )

    def check_if_on_trap(self, traps: list[Trap] = None):
        for trap in traps:
            if np.allclose(self.position, trap.position) and trap.is_alive:
                self.health -= 1
                self.num_of_fallen_traps += 1
                trap.is_alive = False
                break

    def check_if_killed_visible_ghost(self, ghosts_group):
        for qghost in ghosts_group:
            for ghost in qghost.visible_parts:
                if not ghost.is_alive:
                    self.visible_ghosts_killed += 1
