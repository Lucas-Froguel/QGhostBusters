from pygame import Vector2

from src.parameters import ATTACK_RADIUS


def _ghost_in_players_raduis(player_pos:Vector2, ghost_pos: Vector2):
    return (player_pos - ghost_pos).length_squared() <= ATTACK_RADIUS

class Unit:
    def __init__(self, state, position: Vector2, tile: Vector2):
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
            if isinstance(unit, QGhost) and any([newUnitPos == subghost.position for subghost in unit.visible_parts]):
                return

        self.position = newUnitPos


class Player(Unit):
    def __init__(self, state, position: Vector2):
        super().__init__(state, position, Vector2(2, 0))
        self.attack = False


class Ghost(Unit):
    def __init__(self, state, position: Vector2):
        super().__init__(state, position, Vector2(1, 0))


    def move(self, moveVector: Vector2):
        super().move(moveVector)
        #self.check_position()


    def check_position(self):
        """"
        Check whether we are in the zone of application of user's weapon
        """
        player = self.state.player
        if player.attack:
            if _ghost_in_players_raduis(player.position, self.position):
                # TODO: so far it's classical. Replace by quantum
                self.state.units.remove(self)



class QGhost(Unit):
    def __init__(self, game_state, initial_position: Vector2):
        # initialize it in |1>
        self.quantum_state = [1]
        self.visible_parts = [Ghost(state=game_state, position=initial_position)]
        self.n = 1
        self.state = game_state

    def move(self, moveVector: Vector2):
        for subghost in self.visible_parts:
            subghost.move(moveVector)
        self.check_position()

    def check_position(self):
        """"
        Check whether we are in the zone of application of user's weapon
        """
        player = self.state.player
        if player.attack:
            for i in range(self.n):
                if _ghost_in_players_raduis(player.position, self.visible_parts[i].position):
                    # TODO: so far it's classical. Replace by quantum
                    if self.quantum_state[i] == 1:
                        self.quantum_state.pop(i)
                        self.visible_parts.pop(i)
                    else:
                        self.quantum_state[i] -= 1
            if not self.visible_parts:
                self.state.units.remove(self)


