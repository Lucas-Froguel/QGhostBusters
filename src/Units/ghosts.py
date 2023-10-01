import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.settings import GHOST_SPEED


class Ghost(Unit):
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
        self.image = load("src/Units/sprites/ghost.png")
        self.image = scale(self.image, self.cellSize)

    @staticmethod
    def calculate_move_vector() -> Vector2:
        if np.random.random() < GHOST_SPEED:
            return Vector2(0, 0)
        x = np.random.choice([-1, 1])
        y = np.random.choice([-1, 1])
        moveVector = Vector2(x, y)
        return moveVector

    def update(self):
        moveVector = self.calculate_move_vector()
        super().update(moveVector=moveVector)


class QGhost(Ghost):
    """
    A quantum ghost that may be in a superposition.
    Parts of the superposition are implemented as Ghost instances
    """

    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
    ):
        """
        :param cellSize: GameState instance that carries all the info about the game
        :param position: position on the map
        """
        # TODO: it is still classical
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        # initialize it in |1>
        self.quantum_state = [1]
        self.visible_parts = [
            Ghost(cellSize=cellSize, worldSize=worldSize, position=position)
        ]
        self.cellSize = cellSize
