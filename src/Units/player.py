from pygame import Vector2
from pygame.image import load
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.Units.ghosts import QGhost
from src.Units.utils import is_ghost_in_players_radius


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

    def attack(self, ghosts_group: list[QGhost], visible_ghosts_group: RenderUpdates):
        """
        Check whether we are in the zone of application of user's weapon.
        If so, decrease the number of ghosts.

        :param ghosts_group: list of QGhosts present in the game
        :param visible_ghosts_group: visual information about QGhosts
        """
        for qghost in ghosts_group:
            for i, ghost in enumerate(qghost.visible_parts):
                if is_ghost_in_players_radius(self.position, ghost.position):
                    # TODO: so far it's classical. Replace by quantum
                    if qghost.quantum_state[i] == 1:
                        qghost.quantum_state.pop(i)
                        visible_ghosts_group.remove(qghost.visible_parts.pop(i))
                    else:
                        qghost.quantum_state[i] -= 1
            if not qghost.visible_parts:
                ghosts_group.remove(qghost)
