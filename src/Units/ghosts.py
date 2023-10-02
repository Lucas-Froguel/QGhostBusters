import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.Units.splitter import GhostSplitter
from src.Units.utils import two_ghost_coming_from_different_sides_of_splitter
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

    def update(self):
        """ "
        After all the ghosts are in position, we can change their state
        """
        seen = set()
        for splitter in self.splitters:
            for i, this_ghost in enumerate(self.visible_parts[:]):
                if i in seen:
                    continue
                if np.allclose(splitter.position, this_ghost.position, 1e-2):
                    is_coincidence = False
                    for j, other_ghost in enumerate(self.visible_parts[i:]):
                        # check 2 ghosts at the same tile case
                        if two_ghost_coming_from_different_sides_of_splitter(
                            this_ghost, other_ghost, splitter.splitterType
                        ):
                            is_coincidence = True
                            # still classical
                            new_number = (
                                self.quantum_state[i] + self.quantum_state[i + j]
                            )
                            self.quantum_state[i] = new_number
                            self.quantum_state[i + j] = new_number
                            seen |= {i, i + j}
                    if not is_coincidence:
                        new_visual = Ghost(
                            cellSize=self.cellSize,
                            worldSize=self.worldSize,
                            position=this_ghost.position,
                            qghost=self,
                        )
                        new_visual.last_move = (-1) ** (
                            splitter.splitterType == "45"
                        ) * Vector2(this_ghost.last_move.y, this_ghost.last_move.x)

                        self.visible_parts.append(new_visual)
                        self.quantum_state.append(1)
                        self.render_group.add(new_visual)
