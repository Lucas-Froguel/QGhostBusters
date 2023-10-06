
from pygame import Vector2, Surface
from pygame.mixer import Channel

from src.Units.player import Player
from src.Units.ghosts import QGhost
from src.Levels.base_level import BaseLevel
from src.Units.splitter import GhostSplitter
from src.Levels.level_hud import BaseLevelHud
from src.SoundEffects.sound_manager import LevelSoundManager


class CatacombLevel(BaseLevel):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        window: Surface = None,
        level_channel: Channel = None,
        extra_level_channel: Channel = None,
        player_channel: Channel = None,
        enemies_channel: Channel = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel,
        )
        self.level_name = "src/Levels/levels/catacombs.tmx"
        self.level_title = "The Catacombs"

        self.player_initial_position = Vector2(1, 18)
        self.num_ghosts = 3
        self.num_splitters = 4

        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav",
            channel=self.level_channel,
            extra_channel=self.extra_level_channel,
            background_track_path="src/SoundEffects/sound_effects/rain_and_thunder.wav",
        )


class TheMazeLevel(BaseLevel):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        window: Surface = None,
        level_channel: Channel = None,
        extra_level_channel: Channel = None,
        player_channel: Channel = None,
        enemies_channel: Channel = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel
        )
        self.level_name = "src/Levels/levels/the_maze.tmx"
        self.level_title = "The Maze"

        self.player_initial_position = Vector2(1, 10)
        self.num_ghosts = 4
        self.num_splitters = 6

        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav",
            channel=self.level_channel,
            extra_channel=self.extra_level_channel,
            background_track_path="src/SoundEffects/sound_effects/rain_and_thunder.wav",
        )


class IntoTheCavesLevel(BaseLevel):
    def __init__(
            self,
            cellSize: Vector2 = None,
            worldSize: Vector2 = None,
            window: Surface = None,
            level_channel: Channel = None,
            extra_level_channel: Channel = None,
            player_channel: Channel = None,
            enemies_channel: Channel = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel
        )
        self.level_name = "src/Levels/levels/into_the_caves.tmx"
        self.level_title = "Into The Caves"

        self.player_initial_position = Vector2(2, 2)
        self.num_ghosts = 3
        self.num_splitters = 2

        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav",
            channel=self.level_channel,
            extra_channel=self.extra_level_channel,
            background_track_path="src/SoundEffects/sound_effects/rain_and_thunder.wav",
        )


class TheCavesLevel(BaseLevel):
    def __init__(
            self,
            cellSize: Vector2 = None,
            worldSize: Vector2 = None,
            window: Surface = None,
            level_channel: Channel = None,
            extra_level_channel: Channel = None,
            player_channel: Channel = None,
            enemies_channel: Channel = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel
        )
        self.level_name = "src/Levels/levels/the_caves.tmx"
        self.level_title = "The Caves"

        self.player_initial_position = Vector2(1, 10)
        self.num_ghosts = 3
        self.num_splitters = 4

        self.music = LevelSoundManager(
            music="src/SoundEffects/sound_effects/suspense.wav",
            channel=self.level_channel,
            extra_channel=self.extra_level_channel,
            background_track_path="src/SoundEffects/sound_effects/rain_and_thunder.wav",
        )

