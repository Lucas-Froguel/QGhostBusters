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
        self.player_channel = player_channel
        self.enemies_channel = enemies_channel
        self.music: LevelSoundManager = None

        # ghost-splitters
        self.splitter_group: RenderUpdates = RenderUpdates()

        # player and ghosts
        self._player: Player = None
        self.player_group: GroupSingle = GroupSingle()
        self.shots_group: RenderUpdates = RenderUpdates()

        self.ghosts_group: [QGhost] = None
        self.visible_ghosts_group: RenderUpdates = RenderUpdates()

        # to use text blocks
        pygame.font.init()
        self.health_bar_font = pygame.font.SysFont("fonts/Baskic8.otf", 30)

    def update(self):
        self.keep_running = self.user_interface.process_input()

        # visible ghost actions
        self.visible_ghosts_group.update(self._player)

        # player actions
        self.player_group.update(self.user_interface.movePlayerCommand)
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

        if self._player.health <= 0:
            self.keep_running = False
            self.music.play_game_over_sound()
            print("You died")
        if not self.ghosts_group:
            self.keep_running = False
            print("You won")
            self.music.play_game_over_sound()
            return

    def render(self):
        self.window.blit(self.surface, (0, 0))
        self.player_group.draw(self.window)
        self.visible_ghosts_group.draw(self.window)
        self.splitter_group.draw(self.window)
        self.shots_group.draw(self.window)
        health_bar = self.health_bar_font.render(
            f"HP:{self._player.health}", False, (255, 0, 0)
        )
        self.window.blit(health_bar, (0, 0))

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
