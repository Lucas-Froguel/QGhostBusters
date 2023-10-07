from src.Units.ghosts import GhostParameters
from pygame import Vector2, Surface
from pygame.mixer import Channel

from src.Levels.base_level import BaseLevel


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
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel,
            ghost_parameters=ghost_parameters,
        )
        self.level_name = "src/Levels/levels/catacombs.tmx"
        self.level_title = "The Catacombs"

        self.music_path = "src/SoundEffects/sound_effects/suspense.wav"
        self.background_sound_path = (
            "src/SoundEffects/sound_effects/rain_and_thunder.wav"
        )

        self.player_initial_position = Vector2(1, 18)
        self.num_ghosts = 3
        self.num_splitters = 4


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
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel,
            ghost_parameters=ghost_parameters,
        )
        self.level_name = "src/Levels/levels/the_maze.tmx"
        self.level_title = "The Maze"

        self.music_path = "src/SoundEffects/sound_effects/suspense.wav"
        self.background_sound_path = (
            "src/SoundEffects/sound_effects/rain_and_thunder.wav"
        )

        self.player_initial_position = Vector2(1, 10)
        self.num_ghosts = 4
        self.num_splitters = 6


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
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel,
            welcome_message=[
                "Welcome to the game! Please meet the ghosts.",
                "Press Enter to start playing.",
                "Press X to measure ghosts position.",
                "Press Space to shoot.",
                "Press P to pause.",
            ],
            ghost_parameters=ghost_parameters,
        )
        self.level_name = "src/Levels/levels/into_the_caves.tmx"
        self.level_title = "Into The Caves"

        self.music_path = "src/SoundEffects/sound_effects/suspense.wav"
        self.background_sound_path = (
            "src/SoundEffects/sound_effects/rain_and_thunder.wav"
        )

        self.player_initial_position = Vector2(2, 2)
        self.num_ghosts = 3
        self.num_splitters = 2


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
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            window=window,
            level_channel=level_channel,
            extra_level_channel=extra_level_channel,
            player_channel=player_channel,
            enemies_channel=enemies_channel,
            ghost_parameters=ghost_parameters,
        )
        self.level_name = "src/Levels/levels/the_caves.tmx"
        self.level_title = "The Caves"

        self.music_path = "src/SoundEffects/sound_effects/suspense.wav"
        self.background_sound_path = (
            "src/SoundEffects/sound_effects/rain_and_thunder.wav"
        )

        self.player_initial_position = Vector2(1, 10)
        self.num_ghosts = 3
        self.num_splitters = 4
