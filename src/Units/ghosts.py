import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.Units.splitter import GhostSplitter
from src.Units.utils import two_ghost_coming_from_different_size_of_splitter
from src.settings import GHOST_SPEED

DIR_DICT = {"L": (-1, 0), "R": (1, 0), "D": (0, -1), "U": (0, 1)}


class Ghost(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        qghost=None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        :param qghost: meta-ghost of which this one is a part
        """
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        self.image = load("src/Units/sprites/ghost.png")
        self.image = scale(self.image, self.cellSize)
        self.qghost = qghost
        self.index = 0
        self.turn = 0
        self.last_move = Vector2(-1, 0)

    @staticmethod
    def calculate_move_vector() -> Vector2:
        if np.random.random() < GHOST_SPEED:
            return Vector2(0, 0)

        x, y = DIR_DICT[np.random.choice(list(DIR_DICT.keys()))]
        moveVector = Vector2(x, y)
        return moveVector

    def update(self):
        # moveVector = self.calculate_move_vector()
        moveVector = self.last_move
        super().update(moveVector=moveVector)
        self.last_move = moveVector
        self.turn += 1
        qghost = self.qghost
        print(len(qghost.visible_parts), len(qghost.render_group), qghost.quantum_state)
        for splitter in qghost.splitters:
            if np.allclose(splitter.position, self.position, 1e-2):
                for ghost in qghost.visible_parts:
                    # check 2 ghosts at the same tile case
                    if two_ghost_coming_from_different_size_of_splitter(
                        self, ghost, splitter.splitterType
                    ):
                        # still classical
                        new_number = (
                            qghost.quantum_state[self.index]
                            + qghost.quantum_state[ghost.index]
                        )
                        qghost.quantum_state[self.index] = new_number
                        qghost.quantum_state[ghost.index] = new_number
                else:
                    new_position = (
                        self.position
                        # - moveVector
                        + (-1) ** (splitter.splitterType == "45")
                        * Vector2(moveVector.y, moveVector.x)
                    )
                    self.position += moveVector
                    new_visual = Ghost(
                        cellSize=self.cellSize,
                        worldSize=self.worldSize,
                        position=new_position,
                        qghost=qghost,
                    )
                    new_visual.last_move = (-1) ** (
                        splitter.splitterType == "45"
                    ) * Vector2(moveVector.y, moveVector.x)
                    qghost.visible_parts.append(new_visual)
                    qghost.quantum_state.append(1)
                    qghost.render_group.add(new_visual)


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
        splitters: list[GhostSplitter] = None,
        render_group: RenderUpdates = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        :param render_group: a pointer to the visualisation parameters
        """
        # TODO: it is still classical
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        # initialize it in |1>
        self.quantum_state = [1]
        self.visible_parts = [
            Ghost(
                cellSize=cellSize, worldSize=worldSize, position=position, qghost=self
            )
        ]
        self.cellSize = cellSize
        self.splitters = splitters
        self.render_group = render_group
