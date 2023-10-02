from pygame import Vector2, Surface
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates, GroupSingle

from src.Units.player import Player
from src.Units.ghosts import QGhost
from src.Levels.base_level import BaseLevel
from src.Units.splitter import GhostSplitter
from src.SoundEffects.sound_manager import LevelSoundManager


class TestLevel(BaseLevel):
    def __init__(
            self,
            cellSize: Vector2 = None,
            worldSize: Vector2 = None,
            window: Surface = None,
            level_channel: Channel = None,
            unit_channel: Channel = None
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            unit_channel=unit_channel
        )
        self.level_name = "src/Levels/levels/simple_map.tmx"
        self.level_title = "Test Level"
        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav", channel=self.level_channel
        )

    def load_level(self):
        super().load_level()
        self._player = Player(
            cellSize=self.cellSize, worldSize=self.worldSize, position=Vector2(5, 4), channel=self.unit_channel
        )
        self.player_group = GroupSingle()
        self.player_group.add(self._player)

        splitters = [
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(10, 10),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(10, 15),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(5, 10),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(5, 15),
                splitterType="45",
            )
        ]

        self.visible_ghosts_group = RenderUpdates()
        self.ghosts_group = [
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(20, 10),
                splitters=splitters,
                render_group=self.visible_ghosts_group,
            ),
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(10, 16),
                splitters=splitters,
                render_group=self.visible_ghosts_group,
            ),
        ]
        # self.visible_ghosts_group.add(
        #     [ghost.visible_parts for ghost in self.ghosts_group]
        # )

        self.splitter_group = RenderUpdates()
        self.splitter_group.add(splitters)

