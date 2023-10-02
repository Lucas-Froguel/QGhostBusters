import pygame
from pygame import Vector2
from pygame.transform import scale
from src.Levels.levels import TestLevel
from src.user_interfaces import MenuUserInterface


class MainMenu:
    def __init__(self, window=None):
        self.keep_running = True
        self.window = window

        self.menu_items = [
            {"title": "Test Level", "action": lambda: TestLevel},
            {"title": "Quit", "action": lambda: self.exit_menu()},
        ]
        self.current_menu_item = 0
        # Font
        self.titleFont = pygame.font.Font("fonts/BD_Cartoon_Shout.ttf", 72)
        self.itemFont = pygame.font.Font("fonts/BD_Cartoon_Shout.ttf", 48)
        self.menuCursor = pygame.image.load("src/Units/sprites/ghost.png")
        self.menuCursor = scale(self.menuCursor, Vector2(48, 48))

        self.user_interface = MenuUserInterface(
            current_menu_item=self.current_menu_item, menu_items=self.menu_items
        )

    def render(self):
        x, y = self.draw_menu_title()
        menu_width = self.compute_menu_surfaces()
        self.draw_menu_items(x=x, y=y, menu_width=menu_width)

    def update(self):
        self.keep_running = self.user_interface.process_input()

        self.current_menu_item = self.user_interface.current_menu_item
        if self.user_interface.select:
            menu_item = self.menu_items[self.current_menu_item]
            level = menu_item["action"]()
            return level
        elif self.user_interface.quit:
            self.keep_running = False

        return None

    def draw_menu_title(self):
        y = 50
        surface = self.titleFont.render("Qhost Busters!", True, (200, 0, 0))
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
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                self.window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100

    def exit_menu(self):
        self.keep_running = False
