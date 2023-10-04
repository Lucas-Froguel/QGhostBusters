import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.transform import scale
from pytmx import TiledMap


from src.Units.base_unit import Unit


class Weapon(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
        map_data: TiledMap = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        self.map_data = map_data
        self.shots: [Shot] = []
        self.dead_shots: [Shot] = []

    def attack(self, position: Vector2 = None, direction: Vector2 = None):
        self.position = position
        shot = Shot(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=self.position + direction,
            direction=direction,
            channel=self.channel,
            map_data=self.map_data,
        )
        self.shots.append(shot)

    def update(self) -> None:
        alive_shots = []
        dead_shots = []
        for shot in self.shots:
            shot.update()
            if shot.is_alive:
                alive_shots.append(shot)
            else:
                dead_shots.append(shot)

        self.shots = alive_shots
        self.dead_shots = dead_shots


class Shot(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        direction: Vector2 = None,
        channel: Channel = None,
        map_data: TiledMap = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        self.image = load("src/Units/sprites/shot.png")
        self.image = scale(self.image, self.cellSize)
        self.map_data = map_data
        self.direction = direction
        self.is_alive = True

    def collides_with_wall(self):
        walls = self.map_data.layernames["Walls"].tiles()
        for x, y, _ in walls:
            if np.allclose(self.position, Vector2(x, y)):
                return True
        return False

    def update(self) -> None:
        self.move(moveVector=self.direction / 2)
        if not self.is_unit_in_map() or self.collides_with_wall():
            self.is_alive = False
