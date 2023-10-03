from typing import Literal

from pygame import Vector2
from pygame.image import load
from pygame.transform import scale, rotate

from src.Units.base_unit import Unit

# type of the ghost splitter aka degree with respect to X axis
SplitterType = Literal["45", "125"]


class GhostSplitter(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        splitterType: SplitterType = "45",
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        :param type: type of the ghost splitter aka degree with respect to X axis
        """
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        self.image = load(f"src/Units/sprites/splitter_portal_{splitterType}.png")
        self.image = rotate(scale(self.image, self.cellSize), 0)
        self.splitterType = splitterType
