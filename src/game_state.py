import pygame
from pygame import Vector2

from src.Levels.base_level import BaseLevel
from src.Menus.menu import MainMenu


class GameState:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.running = True
        self.clock = pygame.time.Clock()

        # window variables
        self.cellSize: Vector2 = Vector2(32, 32)
        self.worldSize: Vector2 = Vector2(40, 20)
        self.window = None
        self.window_title = "QhostBusters - Menu"
        self.setup_game_window()

        # level variables
        self.level: BaseLevel = None

        self.menu = MainMenu(window=self.window)
        self.setup_game_music(self.menu.music_name)

    def load_level(self, level: BaseLevel):
        self.level = level(
            cellSize=self.cellSize, worldSize=self.worldSize, window=self.window
        )
        self.level.load_level()
        self.setup_game_music(self.level.music_name)

    def unload_level(self):
        self.level = None
        self.setup_game_window()
        self.setup_game_music(self.menu.music_name)

    def setup_game_window(self):
        windowSize = self.cellSize.elementwise() * self.worldSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption(self.window_title)

    @staticmethod
    def setup_game_music(music_name: str):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play(-1)

    def update(
        self,
    ):
        if self.level:
            self.level.update()
            if not self.level.keep_running:
                self.unload_level()
        else:
            level = self.menu.update()
            if level:
                self.load_level(level)
            self.running = self.menu.keep_running

    def render(self):
        self.window.fill((0, 0, 0))
        if self.level:
            self.level.render()
        else:
            self.menu.render()
        pygame.display.update()

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)
