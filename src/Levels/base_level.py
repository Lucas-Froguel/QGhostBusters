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


class BaseLevel:
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        window: Surface = None,
        level_channel: Channel = None,
        unit_channel: Channel = None
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
        self.unit_channel = unit_channel
        self.music: LevelSoundManager = None

        # ghost-splitters
        self.splitter_group: RenderUpdates = None

        # player and ghosts
        self._player: Player = None
        self.player_group: GroupSingle = None

        self.ghosts_group: [QGhost] = None
        self.visible_ghosts_group: RenderUpdates = None

    def update(self):
        self.keep_running = self.user_interface.process_input()

        if not self.ghosts_group:
            self.keep_running = False
            self.music.play_game_over_sound()

        self.player_group.update(self.user_interface.movePlayerCommand)
        self.visible_ghosts_group.update()
        if self.user_interface.attackCommand:
            self._player.measure(self.ghosts_group, self.visible_ghosts_group)
        for qghost in self.ghosts_group:
            qghost.update()

    def render(self):
        self.window.blit(self.surface, (0, 0))
        self.player_group.draw(self.window)
        self.visible_ghosts_group.draw(self.window)
        self.splitter_group.draw(self.window)

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
                    self.surface.blit(image, (x * self.cellSize.x, y * self.cellSize.y))

        self.music.play_music()
