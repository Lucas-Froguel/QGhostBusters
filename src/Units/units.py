import numpy as np
from pygame import Vector2

from src.parameters import ATTACK_RADIUS, GHOST_SPEED


def _ghost_in_players_raduis(player_pos: Vector2, ghost_pos: Vector2) -> bool:
    """ "
    Check whether the ghost is inside player's radius.
    """
    return (player_pos - ghost_pos).length_squared() <= ATTACK_RADIUS**2


class Unit:
    """ "
    Base class for player and ghosts.
    """

    def __init__(self, state, position: Vector2, tile: Vector2):
        """ "
        :param state: GameState instance that carries all the info about the game
        :param position: position on the map
        :param tile: where to take the sprite from on the corresponging png.
        """
        self.state = state
        self.position = position
        self.tile = tile

    def move(self, moveVector: Vector2):
        # Compute new Unit position
        newUnitPos = self.position + moveVector

        # Don't allow positions outside the world
        if (
            newUnitPos.x < 0
            or newUnitPos.x >= self.state.worldSize.x
            or newUnitPos.y < 0
            or newUnitPos.y >= self.state.worldSize.y
        ):
            return

        # Don't allow Player/other Ghost to take a Ghost positions.
        # A Ghost can step on the player though
        for unit in self.state.units:
            if isinstance(unit, Ghost) and newUnitPos == unit.position:
                return
            if isinstance(unit, QGhost) and any(
                [newUnitPos == subghost.position for subghost in unit.visible_parts]
            ):
                return

        self.position = newUnitPos


class Player(Unit):
    def __init__(self, state, position: Vector2):
        """ "
        :param state: GameState instance that carries all the info about the game
        :param position: position on the map
        """
        super().__init__(state, position, Vector2(2, 0))
        self.attack = False  # whether player attacked during this frame


class Ghost(Unit):
    """ "
    A visible ghost, that can be a part of quantum superposition.
    """

    def __init__(self, state, position: Vector2):
        """ "
        :param state: GameState instance that carries all the info about the game
        :param position: position on the map
        """
        super().__init__(state, position, Vector2(1, 0))

    def move(self):
        x = GHOST_SPEED * np.random.choice([-1, 0, 1])
        y = GHOST_SPEED * np.random.choice([-1, 0, 1])
        moveVector = Vector2(x, y)
        super().move(moveVector)
        # self.check_position()

    def check_position(self):
        """ "
        Check whether we are in the zone of application of user's weapon.
        Currently not used
        """
        player = self.state.player
        if player.attack:
            if _ghost_in_players_raduis(player.position, self.position):
                # TODO: so far it's classical. Replace by quantum
                self.state.units.remove(self)


class QGhost(Unit):
    """ "
    A quantum ghost that may be in a superposition.
    Parts of the superposition are implemented as Ghost instances
    """

    def __init__(self, state, initial_position: Vector2):
        """ "
        :param state: GameState instance that carries all the info about the game
        :param initial_position: initial position on the map, before it becomes a superposition.
        """
        # TODO: it is still classical
        # initialize it in |1>
        self.quantum_state = [1]
        self.visible_parts = [Ghost(state=state, position=initial_position)]
        self.n = 1  # number of components
        self.state = state

    def move(self):
        """ "
        Move each visible part
        """
        for subghost in self.visible_parts:
            subghost.move()
        self.check_position()

    def check_position(self):
        """ "
        Check whether we are in the zone of application of user's weapon.
        If so, decrease the number of ghosts.
        """
        player = self.state.player
        if player.attack:
            for i in range(self.n):
                if _ghost_in_players_raduis(
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
