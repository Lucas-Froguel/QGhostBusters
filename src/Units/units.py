from pygame import Vector2


class Unit:
    def __init__(self, state, position, tile):
        self.state = state
        self.position = position
        self.tile = tile

    def move(self, moveVector):
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
            if newUnitPos == unit.position:
                return

        self.position = newUnitPos


class Player(Unit):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(2, 0))


class Ghost(Unit):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(1, 0))
