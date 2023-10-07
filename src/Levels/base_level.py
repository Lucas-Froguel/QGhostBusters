import time
import pytmx
import random
import pygame
from typing import Literal
from pytmx.util_pygame import load_pygame
from pygame import Vector2, Surface
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates, GroupSingle

from src.Units.player import Player
from src.Units.ghosts import QGhost, GhostParameters
from src.Units.trap import Trap
from src.Units.splitter import GhostSplitter
from src.Score.score import ScoreSystem
from src.Levels.level_hud import BaseLevelHud
from src.Levels.utils import generate_random_positions
from src.user_interfaces import GameUserInterface
from src.SoundEffects.sound_manager import LevelSoundManager
from src.settings import MAX_GHOSTS_PER_STATE


class BaseLevel:
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
        score_system: ScoreSystem = None,
        difficulty: int = 3,
    ):
        self.keep_running = True
        self.user_interface = GameUserInterface()
        self.window = window
        self.surface: pygame.Surface = None
        self.level_title: str = "Level"
        self.num_ghosts: int = 1
        self.num_splitters: int = 1
        self.splitter_types: [str] = ["45", "125"]
        self.difficulty: int = difficulty
        self.level_start_time: float = None

        self.cellSize = cellSize
        self.worldSize = worldSize
        self.player_initial_position: Vector2 = None

        self.level_name: str = None
        self.tmx_map: pytmx.TileMap = None
        self.tmx_data = None

        self.music_path: str = None
        self.background_sound_path: str = None
        self.level_channel = level_channel
        self.extra_level_channel = extra_level_channel
        self.player_channel = player_channel
        self.enemies_channel = enemies_channel
        self.music: LevelSoundManager = None

        self.base_level_hud: BaseLevelHud = None

        # ghost-splitters
        self.splitter_group: RenderUpdates = RenderUpdates()

        # player and ghosts
        self._player: Player = None
        self.player_group: GroupSingle = GroupSingle()
        self.shots_group: RenderUpdates = RenderUpdates()
        self.measurement_group: GroupSingle = GroupSingle()

        self.ghost_parameters = ghost_parameters
        self.ghosts_group: [QGhost] = None
        self.visible_ghosts_group: RenderUpdates = RenderUpdates()

        self.traps: [Trap] = []
        self.traps_group = RenderUpdates()

        self.hud_render_group: RenderUpdates = RenderUpdates()

        self.game_status: Literal["won", "lost"] | None = None
        self.scores: ScoreSystem = score_system
        self.level_score: int = 0

    def update(self):
        self.keep_running = self.user_interface.process_input()

        # visible ghost actions
        self.visible_ghosts_group.update(self._player)

        # player actions
        self.player_group.update(
            moveVector=self.user_interface.movePlayerCommand,
            measureCommand=self.user_interface.measureCommand,
            attackCommand=self.user_interface.attackCommand,
            ghosts_group=self.ghosts_group,
            shots_group=self.shots_group,
            traps=self.traps,
        )
        self.measurement_group.update(self._player.position)
        if self.user_interface.attackCommand:
            self.shots_group.add(self._player.weapon.shots)
        self.shots_group.remove(*self._player.weapon.dead_shots)

        # Qhost actions after all the ghosts are in place
        alive_ghosts = []
        for qghost in self.ghosts_group:
            qghost.update(self._player, self.traps)
            if not qghost.is_alive:
                self.ghosts_group.remove(qghost)
                self._player.qghosts_killed += 1
            alive_ghosts += qghost.visible_parts
        self.visible_ghosts_group.remove([ghost for ghost in self.visible_ghosts_group if ghost not in alive_ghosts])

        self.traps_group.add(self.traps)
        self.clean_traps()

        self.base_level_hud.update()

        if self._player.health <= 0:
            self.end_level(status="lost")
        if not self.ghosts_group:
            self.end_level(status="won")

    def end_level(self, status: str = None):
        self.keep_running = False
        self.game_status = status
        self.level_score = self.scores.calculate_score(
            final_health=self._player.health,
            num_of_fallen_traps=self._player.num_of_fallen_traps,
            visible_ghosts_killed=self._player.visible_ghosts_killed,
            qghosts_killed=self._player.qghosts_killed,
            level_difficulty=self.difficulty,
            max_ghosts_per_state=MAX_GHOSTS_PER_STATE,
            total_level_time=time.time() - self.level_start_time,
        )
        if self.game_status == "won":
            self.music.play_game_won_sound()
        else:
            self.music.play_game_over_sound()

    def render(self):
        self.window.blit(self.surface, (0, 0))
        if self.traps:
            self.traps_group.draw(self.window)
        self.player_group.draw(self.window)
        self.visible_ghosts_group.draw(self.window)
        self.splitter_group.draw(self.window)
        self.shots_group.draw(self.window)

        self.hud_render_group.draw(self.window)
        self.base_level_hud.player_data_hud.measure_timer.render()
        self.window.blit(
            self.base_level_hud.player_data_hud.measure_timer.measure_timer, (0, 32)
        )

        if self._player.weapon.measurer.play_animation:
            self.measurement_group.draw(self.window)

    def load_map(self):
        self.tmx_map = pytmx.TiledMap(self.level_name)
        self.tmx_data = load_pygame(self.level_name)

        self.cellSize = Vector2(self.tmx_data.tilewidth, self.tmx_data.tileheight)
        self.worldSize = Vector2(self.tmx_data.width, self.tmx_data.height)

        windowSize = self.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        self.surface = pygame.Surface((int(windowSize.x), int(windowSize.y)))

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    width = image.get_rect().width
                    if width < self.cellSize.x:
                        x_displacement = int(width - self.cellSize.x)
                        self.surface.blit(
                            image,
                            (x * self.cellSize.x, y * self.cellSize.y - x_displacement),
                        )
                    else:
                        self.surface.blit(
                            image, (x * self.cellSize.x, y * self.cellSize.y)
                        )

    def load_units(self):
        splitters = [
            GhostSplitter(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=generate_random_positions(worldSize=self.worldSize),
                splitterType=random.choice(self.splitter_types),
            )
            for _ in range(self.num_splitters)
        ]

        self._player = Player(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=self.player_initial_position,
            channel=self.player_channel,
            map_data=self.tmx_data,
            splitters=splitters,
            does_map_have_tile_dont_pass=True
            if "TileDontPass" in self.tmx_data.layernames
            else False,
        )
        self.player_group.add(self._player)

        self.shots_group.add(self._player.weapon.shots)
        self.measurement_group.add(self._player.weapon.measurer)

        self.ghosts_group = [
            QGhost(
                cellSize=self.cellSize,
                worldSize=self.worldSize,
                position=generate_random_positions(
                    worldSize=self.worldSize,
                    player_position=self.player_initial_position,
                ),
                splitters=splitters,
                render_group=self.visible_ghosts_group,
                channel=self.enemies_channel,
                ghost_parameters=self.ghost_parameters,
            )
            for _ in range(self.num_ghosts)
        ]

        self.splitter_group.add(splitters)

        self.base_level_hud = BaseLevelHud(cellSize=self.cellSize, player=self._player)
        self.hud_render_group.add(self.base_level_hud.player_data_hud.hearts)

    def load_music(self):
        self.music = LevelSoundManager(
            music=self.music_path,
            channel=self.level_channel,
            extra_channel=self.extra_level_channel,
            background_track_path=self.background_sound_path,
        )

    def load_level(self):
        self.load_music()
        self.music.play_load_level_sound()
        self.load_map()
        self.load_units()
        self.music.play_music()
        self.level_start_time = time.time()

    def clean_traps(self):
        for trap in self.traps:
            if not trap.is_alive:
                self.traps_group.remove(trap)
                self.traps.remove(trap)
        # add new ones
        self.traps_group.add(self.traps)
