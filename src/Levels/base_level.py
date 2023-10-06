
from typing import Literal

import pytmx
from pytmx.util_pygame import load_pygame
import pygame
from pygame import Vector2, Surface
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates, GroupSingle

from src.Units.player import Player
from src.Units.ghosts import QGhost
from src.user_interfaces import GameUserInterface
from src.SoundEffects.sound_manager import LevelSoundManager
from src.Levels.level_hud import BaseLevelHud


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

    ):
        self.keep_running = True
        self.user_interface = GameUserInterface()
        self.window = window
        self.surface: pygame.Surface = None
        self.level_title: str = "Level"

        self.cellSize = cellSize
        self.worldSize = worldSize

        self.level_name: str = None
        self.tmx_map: pytmx.TileMap = None
        self.tmx_data = None

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

        self.ghosts_group: [QGhost] = None
        self.visible_ghosts_group: RenderUpdates = RenderUpdates()

        self.hud_render_group: RenderUpdates = RenderUpdates()

        self.game_status: Literal["won", "lost"] | None = None

    def update(self):
        self.keep_running = self.user_interface.process_input()

        # visible ghost actions
        self.visible_ghosts_group.update(self._player)

        # player actions
        self.player_group.update(self.user_interface.movePlayerCommand)
        self.measurement_group.update(self._player.position)
        if self.user_interface.measureCommand:
            self._player.measure(self.ghosts_group)  # wave func collapse
        elif self.user_interface.attackCommand:
            self._player.attack()
            self.shots_group.add(self._player.weapon.shots)
        self.shots_group.remove(*self._player.weapon.dead_shots)

        # Qhost actions after all the ghosts are in place
        for qghost in self.ghosts_group:
            qghost.update(self._player)
            if not qghost.is_alive:
                self.ghosts_group.remove(qghost)

        self.base_level_hud.update()

        if self._player.health <= 0:
            self.keep_running = False
            self.music.play_game_over_sound()
            self.game_status = "lost"
        if not self.ghosts_group:
            self.keep_running = False
            self.music.play_game_won_sound()
            self.game_status = "won"
            return

    def render(self):
        self.window.blit(self.surface, (0, 0))
        self.player_group.draw(self.window)
        self.visible_ghosts_group.draw(self.window)
        self.splitter_group.draw(self.window)
        self.shots_group.draw(self.window)

        self.hud_render_group.draw(self.window)
        self.base_level_hud.player_data_hud.measure_timer.render()
        self.window.blit(self.base_level_hud.player_data_hud.measure_timer.measure_timer, (0, 32))

        if self._player.weapon.measurer.play_animation:
            self.measurement_group.draw(self.window)

    def load_map(self):
        self.tmx_map = pytmx.TiledMap(self.level_name)
        self.tmx_data = load_pygame(self.level_name)

    def load_level(self):
        self.music.play_load_level_sound()
        self.load_map()
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
                        self.surface.blit(image, (x * self.cellSize.x, y * self.cellSize.y - x_displacement))
                    else:
                        self.surface.blit(image, (x * self.cellSize.x, y * self.cellSize.y))

        self.music.play_music()
