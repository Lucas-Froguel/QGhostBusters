import pygame
from pygame import Vector2
from src.Levels.base_level import BaseLevel
from src.Menus.menu import MenusManager
from src.SoundEffects.sound_manager import ScreenSoundManager
from src.Units.ghosts import GhostParameters
from src.Score.score import ScoreSystem


class GameState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer_music.set_volume(0.1)
        pygame.mixer.set_num_channels(4)
        self.window_channel = pygame.mixer.Channel(0)
        self.extra_level_channel = pygame.mixer.Channel(1)
        self.player_channel = pygame.mixer.Channel(2)
        self.enemies_channel = pygame.mixer.Channel(3)

        self.running = True
        self.clock = pygame.time.Clock()

        # window variables
        self.cellSize: Vector2 = Vector2(32, 32)
        self.worldSize: Vector2 = Vector2(40, 20)
        self.window = None
        self.window_title = "QhostBusters - Menu"
        self.setup_game_window()

        self.score_system = ScoreSystem()

        # level variables
        self.level: BaseLevel = None

        self.menu = MenusManager(
            window=self.window,
            channel=self.window_channel,
            score_system=self.score_system,
        )
        self.setup_game_music(self.menu.music)
        self.last_game_status: str = None
        self.last_game_score: int = None
        self.last_game_id: str = None
        self.last_game_name: str = None
        self.has_level_ended: bool = False

    def load_level(self, level: BaseLevel, ghost_parameters: GhostParameters = None):
        self.last_game_status = None
        self.has_level_ended = False
        self.level = level(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            window=self.window,
            level_channel=self.window_channel,
            extra_level_channel=self.extra_level_channel,
            player_channel=self.player_channel,
            enemies_channel=self.enemies_channel,
            ghost_parameters=ghost_parameters,
            score_system=self.score_system,
        )
        self.level.load_level()
        self.last_game_id = self.level.level_id
        self.last_game_name = self.level.level_title

    def unload_level(self):
        self.last_game_score = self.level.level_score
        self.level = None
        self.setup_game_window()
        self.setup_game_music(self.menu.music)
        self.has_level_ended = True

    def setup_game_window(self):
        windowSize = self.cellSize.elementwise() * self.worldSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption(self.window_title)

    @staticmethod
    def setup_game_music(music: ScreenSoundManager):
        music.play_music()

    def update(
        self,
    ):
        if self.level:
            self.level.update()
            if not self.level.keep_running:
                self.last_game_status = self.level.game_status
                self.unload_level()
        else:
            if self.has_level_ended:
                if self.last_game_status == "won":
                    self.menu.current_menu = "won_message"
                elif self.last_game_status == "lost":
                    self.menu.current_menu = "lost_message"
                self.has_level_ended = False

            level = self.menu.update(
                level_score=self.last_game_score,
                level_id=self.last_game_id,
                level_name=self.last_game_name,
                level_message=f"{self.last_game_status}_message",
            )
            if level:
                self.load_level(level, self.menu.settings.ghost_parameters)
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
