import numpy as np
from pygame import Vector2, Rect
from pygame.mixer import Channel
from pytmx import TiledMap

from src.Units.base_unit import Unit, AnimatedUnit


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
        self.measurer = Measurement(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )

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


class Shot(AnimatedUnit):
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
            cellSize=cellSize,
            worldSize=worldSize,
            position=position,
            channel=channel,
            images_folder="src/Units/sprites/shots",
            images_name="shot",
        )

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

        self.update_image()


class Measurement(AnimatedUnit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """
        super().__init__(
            cellSize=10 * cellSize,
            worldSize=worldSize,
            position=position,
            channel=channel,
            images_folder="src/Units/sprites/measurements",
            images_name="measurement",
        )
        self.play_animation = False
        self.regularCellSize = cellSize
        self.rect = Rect(
            self.position.x * cellSize.x,
            self.position.y * cellSize.y,
            self.cellSize.x,
            self.cellSize.y,
        )

    def calculate_rect(self):
        self.rect = Rect(
            self.position.x * self.regularCellSize.x - self.cellSize.x / 2,
            self.position.y * self.regularCellSize.y - self.cellSize.y / 2,
            self.cellSize.x,
            self.cellSize.y,
        )

    def update_position(self, position: Vector2 = None):
        self.position = position

    def update_image(self):
        self.image = self.images[int(self.current_image_index)]
        self.current_image_index += self.current_image_direction

    def measure(self, position: Vector2 = None):
        self.play_animation = True
        self.update_position(position=position)
        self.calculate_rect()

    def stop_animation(self):
        if int(self.current_image_index) == self.num_images:
            self.play_animation = False
            self.current_image_index = 0

    def update(self, moveVector: Vector2 = None):
        # super().update()
        # self.update_position(moveVector=moveVector)
        self.stop_animation()
        if self.play_animation:
            self.update_image()
