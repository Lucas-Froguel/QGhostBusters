from pygame import Vector2
from pygame.image import load
from pygame.transform import scale
from src.Units.base_unit import Unit


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
