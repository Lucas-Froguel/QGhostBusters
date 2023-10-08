import pygame
from pygame.image import load
from pygame.mixer import Channel
from pygame.transform import scale
from pygame import Vector2, Surface
from src.Units.ghosts import GhostParameters

from src.settings import PROB_GHOST_TRAP, PROB_GHOST_ATTACK, MAX_DIFFICULTY
from src.Levels.levels import (
    CatacombLevel,
    TheMazeLevel,
    IntoTheCavesLevel,
    TheCavesLevel,
)
from src.user_interfaces import (
    MenuUserInterface,
    SettingsMenuUserInterface,
    EnterTextUserInterface,
)

from src.SoundEffects.sound_manager import MenuSoundManager
from src.Score.score import ScoreSystem


class BaseMenu:
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        self.keep_running = True
        self.should_exit = False
        self.current_menu = "main_menu"
        self.window = window
        self.music = music

        self.title: str = None
        self.menu_items: dict = None
        self.current_menu_item = 0
        # Font
        self.titleFont = pygame.font.Font("fonts/Baskic8.otf", 72)
        self.itemFont = pygame.font.Font("fonts/Baskic8.otf", 48)
        self.menuCursor = pygame.image.load("src/Units/sprites/ghost.png")
        self.menuCursor = scale(self.menuCursor, Vector2(48, 48))

        self.background = load("src/Menus/backgrounds/background_menu.png")

        self.user_interface: MenuUserInterface = None

    def load_menu(self):
        self.current_menu = self.current_menu

    def render(self):
        self.window.blit(self.background, (0, 0))
        x, y = self.draw_menu_title()
        menu_width = self.compute_menu_surfaces()
        self.draw_menu_items(x=x, y=y, menu_width=menu_width)

    def update(self, **kwargs):
        self.keep_running = self.user_interface.process_input()

        self.current_menu_item = self.user_interface.current_menu_item
        if self.user_interface.quit:
            self.keep_running = False

    def draw_menu_title(self):
        y = 50
        surface = self.titleFont.render(self.title, True, (200, 0, 0))
        x = (self.window.get_width() - surface.get_width()) // 2
        self.window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100
        return x, y

    def compute_menu_surfaces(self):
        menu_width = 0
        for item in self.menu_items:
            surface = self.itemFont.render(item["title"], True, (200, 0, 0))
            menu_width = max(menu_width, surface.get_width())
            item["surface"] = surface

        return menu_width

    def draw_menu_items(self, menu_width: float = None, x: float = 0, y: float = 0):
        x = (self.window.get_width() - menu_width) // 2
        for index, item in enumerate(self.menu_items):
            # Item text
            surface = item["surface"]
            self.window.blit(surface, (x, y))

            # Cursor
            if index == self.current_menu_item:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = (
                    y + (surface.get_height() - self.menuCursor.get_height()) // 2 - 10
                )
                self.window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100

    def exit_menu(self):
        self.keep_running = False


class MenusManager:
    def __init__(
        self,
        window: Surface = None,
        channel: Channel = None,
        score_system: ScoreSystem = None,
    ):
        self.window = window
        self.channel = channel
        self.current_menu = "main_menu"
        self.keep_running = True
        self.music = MenuSoundManager(channel=self.channel)
        ghost_parameters = GhostParameters()
        self.main_menu = MainMenu(window=self.window, music=self.music)
        self.settings = SettingsMenu(
            window=self.window, music=self.music, ghost_parameters=ghost_parameters
        )
        self.levels = LevelsMenu(
            window=self.window,
            music=self.music,
            ghost_parameters=self.settings.ghost_parameters,
        )

        self.win_message = WinMessage(window=window, music=self.music)
        self.lose_message = LoseMessage(window=window, music=self.music)
        self.enter_name = EnterNameMenu(
            window=window, music=self.music, scores=score_system
        )

        self.highscores = DisplayHighScores(
            window=window, music=self.music, scores=score_system
        )

        self.into_the_caves = LevelHighScores(
            window=self.window,
            music=self.music,
            level_name="Into The Caves",
            level_id="into_the_caves",
            scores=score_system,
        )
        self.the_caves = LevelHighScores(
            window=self.window,
            music=self.music,
            level_name="The Caves",
            level_id="the_caves",
            scores=score_system,
        )
        self.the_catacombs = LevelHighScores(
            window=self.window,
            music=self.music,
            level_name="The Catacombs",
            level_id="the_catacombs",
            scores=score_system,
        )
        self.the_maze = LevelHighScores(
            window=self.window,
            music=self.music,
            level_name="The Maze",
            level_id="the_maze",
            scores=score_system,
        )

        self.possible_menus = {
            "main_menu": self.main_menu,
            "settings": self.settings,
            "levels": self.levels,
            "won_message": self.win_message,
            "lost_message": self.lose_message,
            "enter_name": self.enter_name,
            "highscores": self.highscores,
            "into_the_caves": self.into_the_caves,
            "the_caves": self.the_caves,
            "the_catacombs": self.the_catacombs,
            "the_maze": self.the_maze,
        }

    def update(self, **kwargs):
        current_menu_class = self.possible_menus[self.current_menu]
        self.keep_running = current_menu_class.keep_running
        if self.current_menu != current_menu_class.current_menu:
            self.current_menu = current_menu_class.current_menu
            current_menu_class.load_menu()
        level = current_menu_class.update(**kwargs)
        return level

    def render(self):
        self.possible_menus[self.current_menu].render()


class MainMenu(BaseMenu):
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        super().__init__(window=window, music=music)

        self.title = "Qhost Busters!"
        self.menu_items = [
            {"title": "Levels", "action": lambda: self.load_levels_menu()},
            {"title": "Highscores", "action": lambda: self.load_highscores_menu()},
            {"title": "Settings", "action": lambda: self.load_settings_menu()},
            {"title": "Quit", "action": lambda: self.exit_menu()},
        ]

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )

    def update(self, **kwargs):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()

    def load_settings_menu(self):
        self.current_menu = "settings"

    def load_levels_menu(self):
        self.current_menu = "levels"

    def load_highscores_menu(self):
        self.current_menu = "highscores"

    def load_menu(self, **kwargs):
        self.current_menu = "main_menu"


class LevelsMenu(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(window=window, music=music)

        self.current_menu = "levels"
        self.title = "Levels"
        self.menu_items = [
            {"title": "Into The Caves", "action": lambda: IntoTheCavesLevel},
            {"title": "The Caves", "action": lambda: TheCavesLevel},
            {"title": "The Catacombs", "action": lambda: CatacombLevel},
            {"title": "The Maze", "action": lambda: TheMazeLevel},
            {"title": "Back", "action": lambda: self.exit_settings()},
        ]
        self.ghost_parameters = ghost_parameters
        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )
        self.should_exit_settings = False

    def update(self, **kwargs):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            level = menu_item["action"]()
            return level

    def exit_settings(self):
        self.current_menu = "main_menu"

    def load_menu(self, **kwargs):
        self.current_menu = "levels"


class SettingsMenu(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
        ghost_parameters: GhostParameters = None,
    ):
        super().__init__(window=window, music=music)

        self.current_menu = "settings"
        self.title = "Settings"
        self.volume = 100
        self.difficulty = MAX_DIFFICULTY - 2
        self.ghost_parameters = ghost_parameters
        self.menu_items = [
            {"title": f"Volume - {self.volume}", "action": lambda: None},
            {"title": f"Difficutly - {self.difficulty}", "action": lambda: None},
            {"title": "Back", "action": lambda: self.exit_settings()},
        ]

        self.user_interface = SettingsMenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
            volume=self.volume,
            difficulty=self.difficulty,
        )
        self.should_exit_settings = False

    def change_volume(self):
        pygame.mixer_music.set_volume(self.volume / (100 * 2))

    def exit_settings(self):
        self.current_menu = "main_menu"

    def load_menu(self):
        self.current_menu = "settings"

    def update(self, **kwargs):
        self.compute_menu_surfaces()
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()
        if self.volume != self.user_interface.volume:
            self.volume = self.user_interface.volume
            self.menu_items[0]["title"] = f"Volume - {self.volume}"
            self.change_volume()
        if self.difficulty != self.user_interface.difficulty:
            self.difficulty = self.user_interface.difficulty
            self.menu_items[1]["title"] = f"Difficulty - {self.difficulty}"
            self.change_difficulty()

    def change_difficulty(self):
        self.ghost_parameters.change_difficulty(difficulty=self.difficulty)
        self.ghost_parameters.trap_probability = (
            PROB_GHOST_TRAP * self.difficulty / MAX_DIFFICULTY
        )
        self.ghost_parameters.attack_probability = (
            PROB_GHOST_ATTACK * self.difficulty / MAX_DIFFICULTY
        )


class LoseMessage(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
    ):
        super().__init__(window=window, music=music)
        self.level_score: int = None
        self.title = "You were annihilated!"
        self.current_menu = "lost_message"
        self.menu_items = [
            {"title": f"Score: {self.level_score}", "action": lambda: None},
            {"title": "Enter your name", "action": lambda: self.load_enter_name()},
            {"title": "Go back to menu", "action": lambda: self.exit_message()},
        ]

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )

    def update(self, **kwargs):
        self.level_score = kwargs["level_score"]

        self.menu_items[0]["title"] = f"Score: {self.level_score}"
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()

    def exit_message(self):
        self.current_menu = "levels"

    def load_menu(self, **kwargs):
        self.current_menu = "lost_message"

    def load_enter_name(
        self,
    ):
        self.current_menu = "enter_name"


class WinMessage(LoseMessage):
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        super().__init__(window=window, music=music)
        self.current_menu = "won_message"
        self.title = "You won!"

    def load_menu(self, **kwargs):
        self.current_menu = "won_message"


class EnterNameMenu(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
        level_message: str = None,
        scores: ScoreSystem = None,
    ):
        super().__init__(window=window, music=music)
        self.level_score: int = None
        self.level_id: str = None
        self.level_name: str = None
        self.title = "Enter your name"
        self.current_menu = "enter_name"
        self.level_message = level_message
        self.name: str = ""

        self.menu_items = [
            {"title": self.name, "action": lambda: self.exit_message()},
        ]

        self.user_interface = EnterTextUserInterface()
        self.scores = scores

    def exit_message(self):
        self.current_menu = self.level_message

    def update(self, **kwargs):
        self.level_score = kwargs["level_score"]
        self.level_id = kwargs["level_id"]
        self.level_name = kwargs["level_name"]
        self.level_message = kwargs["level_message"]

        self.name = self.user_interface.text
        self.menu_items[0]["title"] = self.name
        if not self.user_interface.process_input():
            self.scores.add_score(
                map_id=self.level_id, score=self.level_score, player_name=self.name
            )
            self.scores.save_scores()
            self.exit_message()


class DisplayHighScores(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
        scores: ScoreSystem = None,
    ):
        super().__init__(window=window, music=music)
        self.scores = scores
        self.title = "Highscores"
        self.current_menu = "highscores"

        self.menu_items = [
            {
                "title": "Into The Caves",
                "action": lambda: self.load_into_the_caves_highscores(),
            },
            {"title": "The Caves", "action": lambda: self.load_the_caves_highscores()},
            {
                "title": "The Catacombs",
                "action": lambda: self.load_the_catacombs_highscores(),
            },
            {"title": "The Maze", "action": lambda: self.load_the_maze_highscores()},
            {"title": "Back to menu", "action": lambda: self.exit_message()},
        ]

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )

    def load_into_the_caves_highscores(self):
        self.current_menu = "into_the_caves"

    def load_the_caves_highscores(self):
        self.current_menu = "the_caves"

    def load_the_catacombs_highscores(self):
        self.current_menu = "the_catacombs"

    def load_the_maze_highscores(self):
        self.current_menu = "the_maze"

    def load_menu(self):
        self.current_menu = "highscores"

    def exit_message(self):
        self.current_menu = "main_menu"

    def update(self, **kwargs):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()


class LevelHighScores(BaseMenu):
    def __init__(
        self,
        window: Surface = None,
        music: MenuSoundManager = None,
        scores: ScoreSystem = None,
        level_name: str = None,
        level_id: str = None,
    ):
        super().__init__(window=window, music=music)
        self.title = f"Highscores - {level_name}"
        self.level_id = level_id
        self.current_menu = level_id
        self.scores = scores
        self.actual_scores = self.scores.return_high_scores(map_id=self.current_menu)

        self.menu_items = [
            {"title": f"{score[0]} - {score[1]}", "action": lambda: None}
            for score in self.actual_scores
        ]
        self.menu_items.append(
            {"title": "Back to Highscores", "action": lambda: self.exit_message()},
        )

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )

    def exit_message(self):
        self.current_menu = "highscores"

    def update(self, **kwargs):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()

        actual_scores = self.scores.return_high_scores(map_id=self.level_id)
        if actual_scores != self.actual_scores:
            self.menu_items = [
                {"title": f"{score[0]} - {score[1]}"} for score in actual_scores
            ]
            self.menu_items.append(
                {"title": "Back to Highscores", "action": lambda: self.exit_message()},
            )
            self.user_interface = MenuUserInterface(
                current_menu_item=self.current_menu_item,
                menu_items=self.menu_items,
                music=self.music,
            )

    def load_menu(self):
        self.current_menu = self.level_id
