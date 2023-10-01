import numpy as np
from pygame import Vector2
from pygame.image import load
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.settings import GHOST_SPEED
from src.Units.utils import is_ghost_in_players_radius


class Ghost(Unit):
    def __init__(self, cellSize: Vector2 = None, worldSize: Vector2 = None, position: Vector2 = None):
        """
        :param cellSize: GameState instance that carries all the info about the game
        :param position: position on the map
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

    def __init__(self, cellSize: Vector2 = None, worldSize: Vector2 = None, position: Vector2 = None):
        """
        :param state: GameState instance that carries all the info about the game
        :param initial_position: initial position on the map, before it becomes a superposition.
        """
        # TODO: it is still classical
        super().__init__(cellSize=cellSize, worldSize=worldSize, position=position)
        # initialize it in |1>
        self.quantum_state = [1]
        self.visible_parts = [Ghost(cellSize=cellSize, worldSize=worldSize, position=position)]
        self.n = 1  # number of components
        self.cellSize = cellSize

    def update(self, player):
        """
        Move each visible part
        """
        for subghost in self.visible_parts:
            subghost.update()
        self.check_position(player)

    def check_position(self, player):
        """
        Check whether we are in the zone of application of user's weapon.
        If so, decrease the number of ghosts.
        """
        if player.attack:
            for i in range(self.n):
                if is_ghost_in_players_radius(
                        player.position, self.visible_parts[i].position
                ):
                    # TODO: so far it's classical. Replace by quantum
                    if self.quantum_state[i] == 1:
                        self.quantum_state.pop(i)
                        self.visible_parts.pop(i)
                    else:
                        self.quantum_state[i] -= 1
            if not self.visible_parts:
                self.state.units.remove(self)

