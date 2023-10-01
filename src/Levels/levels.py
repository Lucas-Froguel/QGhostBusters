from pygame import Vector2
from pygame.sprite import RenderUpdates, GroupSingle

from src.Units.player import Player
from src.Units.ghosts import QGhost
from src.Levels.base_level import BaseLevel


class TestLevel(BaseLevel):
    def __init__(
        self, cellSize: Vector2 = None, worldSize: Vector2 = None, window=None
    ):
        super().__init__(cellSize=cellSize, worldSize=worldSize, window=window)

        self.level_name = "src/Levels/levels/simple_map.tmx"
        self.level_title = "Test Level"

    def load_level(self):
        super().load_level()
        self._player = Player(
            cellSize=self.cellSize, worldSize=self.worldSize, position=Vector2(5, 4)
        )
        self.player_group = GroupSingle()
        self.player_group.add(self._player)

        self.ghosts_group = [
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(20, 10),
            ),
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(10, 16),
            ),
        ]
        self.visible_ghosts_group = RenderUpdates()
        # not good, because if more visible ghosts appear, they won't be here, think more
        self.visible_ghosts_group.add(
            [ghost.visible_parts for ghost in self.ghosts_group]
        )
