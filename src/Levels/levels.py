from pygame import Vector2, Surface
from pygame.mixer import Channel, find_channel

from src.Units.player import Player
from src.Units.ghosts import QGhost
from src.Levels.base_level import BaseLevel
from src.Units.splitter import GhostSplitter
from src.SoundEffects.sound_manager import LevelSoundManager


class CatacombLevel(BaseLevel):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        window: Surface = None,
        level_channel: Channel = None,
        unit_channel: Channel = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            unit_channel=unit_channel,
        )
        self.level_name = "src/Levels/levels/catacombs.tmx"
        self.level_title = "The Catacombs"
        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav",
            channel=self.level_channel,
            extra_channel=find_channel(),
            background_track_path="src/SoundEffects/sound_effects/rain_and_thunder.wav",
        )

    def load_level(self):
        super().load_level()
        splitters = [
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(35, 5),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(30, 15),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(20, 10),
                splitterType="45",
            ),
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(5, 15),
                splitterType="45",
            ),
        ]

        self._player = Player(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=Vector2(5, 4),
            channel=self.unit_channel,
            map_data=self.tmx_data,
            splitters=splitters,
        )
        self.player_group.add(self._player)

        self.shots_group.add(self._player.weapon.shots)

        self.ghosts_group = [
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(20, 10),
                splitters=splitters,
                render_group=self.visible_ghosts_group,
                channel=self.unit_channel,
            ),
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=Vector2(10, 16),
                splitters=splitters,
                render_group=self.visible_ghosts_group,
                channel=self.unit_channel,
            ),
        ]

        self.splitter_group.add(splitters)
