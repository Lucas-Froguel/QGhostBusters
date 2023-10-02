import math
from pygame import Vector2
from pygame.image import load
from pygame.transform import scale
from pygame.transform import rotate
from src.Units.base_unit import Unit


class Player(Unit):
    def __init__(self, cellSize: Vector2 = None, worldSize: Vector2 = None, position: Vector2 = None):
        """ "
        :param worldSize: GameState instance that carries all the info about the game
        :param position: position on the map
        """
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        self.attack = False
        self.image = load("src/Units/sprites/player.png")
        self.image = scale(self.image, self.cellSize)
        self.direction: Vector2 = Vector2(1, 0)

    def move(self, moveVector: Vector2) -> None:
        super().move(moveVector=moveVector)

        angle = math.acos(self.direction.dot(moveVector) / (self.direction.length() * moveVector.length()))
        self.direction = moveVector
        self.image = rotate(self.image, -math.degrees(angle))
