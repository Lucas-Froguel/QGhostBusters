import pygame
from pygame.image import load
from pygame.mixer import Channel
from pygame.transform import scale
from pygame import Vector2, Surface
from src.Levels.levels import CatacombLevel
from src.user_interfaces import MenuUserInterface, SettingsMenuUserInterface
from src.SoundEffects.sound_manager import MenuSoundManager


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
        self.menuCursor = pygame.image.load("src/Units/sprites/new_ghost2.png")
        self.menuCursor = scale(self.menuCursor, Vector2(48, 48))

        self.background = load("src/Menus/background_menu.png")

        self.user_interface: MenuUserInterface = None

    def render(self):
        self.window.blit(self.background, (0, 0))
        x, y = self.draw_menu_title()
        menu_width = self.compute_menu_surfaces()
        self.draw_menu_items(x=x, y=y, menu_width=menu_width)

    def update(self):
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
    def __init__(self, window: Surface = None, channel: Channel = None):
        self.window = window
        self.channel = channel
        self.current_menu = "main_menu"
        self.keep_running = True
        self.music = MenuSoundManager(channel=self.channel)

        self.main_menu = MainMenu(window=self.window, music=self.music)
        self.settings = SettingsMenu(window=self.window, music=self.music)
        self.levels = LevelsMenu(window=self.window, music=self.music)

        self.possible_menus = {
            "main_menu": self.main_menu,
            "settings": self.settings,
            "levels": self.levels,
        }

    def update(self):
        current_menu_class = self.possible_menus[self.current_menu]
        self.keep_running = current_menu_class.keep_running
        if self.current_menu != current_menu_class.current_menu:
            self.current_menu = current_menu_class.current_menu
            current_menu_class.load_menu()
        level = current_menu_class.update()
        return level

    def render(self):
        self.possible_menus[self.current_menu].render()


class MainMenu(BaseMenu):
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        super().__init__(window=window, music=music)

        self.title = "Qhost Busters!"
        self.menu_items = [
            {"title": "Levels", "action": lambda: self.load_levels_menu()},
            {"title": "Settings", "action": lambda: self.load_settings_menu()},
            {"title": "Quit", "action": lambda: self.exit_menu()},
        ]

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )

    def update(self):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()

    def load_settings_menu(self):
        self.current_menu = "settings"

    def load_levels_menu(self):
        self.current_menu = "levels"

    def load_menu(self):
        self.current_menu = "main_menu"


class LevelsMenu(BaseMenu):
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        super().__init__(window=window, music=music)

        self.current_menu = "levels"
        self.title = "Levels"
        self.menu_items = [
            {"title": "The Catacombs", "action": lambda: CatacombLevel},
            {"title": "Back", "action": lambda: self.exit_settings()},
        ]

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
        )
        self.should_exit_settings = False

    def update(self):
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            level = menu_item["action"]()
            return level

    def exit_settings(self):
        self.current_menu = "main_menu"

    def load_menu(self):
        self.current_menu = "levels"


class SettingsMenu(BaseMenu):
    def __init__(self, window: Surface = None, music: MenuSoundManager = None):
        super().__init__(window=window, music=music)

        self.current_menu = "settings"
        self.title = "Settings"
        self.volume = 100
        self.menu_items = [
            {"title": f"Volume - {self.volume}", "action": lambda: None},
            {"title": "Back", "action": lambda: self.exit_settings()},
        ]

        self.user_interface = SettingsMenuUserInterface(
            current_menu_item=self.current_menu_item,
            menu_items=self.menu_items,
            music=self.music,
            volume=self.volume,
        )
        self.should_exit_settings = False

    def change_volume(self):
        pygame.mixer_music.set_volume(self.volume / (100 * 2))

    def exit_settings(self):
        self.current_menu = "main_menu"

    def load_menu(self):
        self.current_menu = "settings"

    def update(self):
        self.compute_menu_surfaces()
        super().update()
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            menu_item["action"]()
        if self.volume != self.user_interface.volume:
            self.volume = self.user_interface.volume
            self.menu_items[0]["title"] = f"Volume - {self.volume}"
            self.change_volume()
