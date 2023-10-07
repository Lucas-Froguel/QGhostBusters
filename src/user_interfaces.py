import pygame
from pygame import Vector2

from src.settings import MAX_DIFFICULTY


class BaseUserInterface:
    def process_input(self):
        pass


class MenuUserInterface(BaseUserInterface):
    def __init__(
        self, current_menu_item: int = None, menu_items: [dict] = None, music=None
    ):
        self.current_menu_item = current_menu_item
        self.menu_items = menu_items
        self.select = False
        self.quit = False
        self.running = True
        self.music = music

    def process_input(self):
        self.select = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.current_menu_item += 1
                    self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_UP:
                    self.current_menu_item -= 1
                    self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_RETURN:
                    self.select = True
                self.current_menu_item %= len(self.menu_items)
        return self.running


class SettingsMenuUserInterface(BaseUserInterface):
    def __init__(
        self,
        current_menu_item: int = None,
        menu_items: [dict] = None,
        music=None,
        volume: float = None,
        difficulty: int = None,
    ):
        self.current_menu_item = current_menu_item
        self.menu_items = menu_items
        self.select = False
        self.quit = False
        self.running = True
        self.music = music
        self.volume = volume
        self.difficulty = difficulty

    def process_input(self):
        self.select = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.current_menu_item += 1
                    self.music.play_select_menu_item_sound()
                    self.current_menu_item %= len(self.menu_items)
                elif event.key == pygame.K_UP:
                    self.current_menu_item -= 1
                    self.music.play_select_menu_item_sound()
                    self.current_menu_item %= len(self.menu_items)
                elif event.key == pygame.K_LEFT and self.current_menu_item == 0:
                    if self.volume > 0:
                        self.volume -= 5
                elif event.key == pygame.K_LEFT and self.current_menu_item == 1:
                    if self.difficulty > 1:
                        self.difficulty -= 1
                elif event.key == pygame.K_RIGHT and self.current_menu_item == 0:
                    if self.volume < 100:
                        self.volume += 5
                elif event.key == pygame.K_RIGHT and self.current_menu_item == 1:
                    if self.difficulty < MAX_DIFFICULTY:
                        self.difficulty += 1
                elif event.key == pygame.K_RETURN:
                    self.select = True
        return self.running


class EnterTextUserInterface(BaseUserInterface):
    def __init__(self):
        self.select = False
        self.quit = False
        self.running = True
        self.text: str = ""

    def process_input(self):
        self.running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        return self.running


class GameUserInterface(BaseUserInterface):
    def __init__(self):
        self.movePlayerCommand = Vector2(0, 0)
        self.attackCommand = False
        self.measureCommand = False

    def process_input(self):
        self.movePlayerCommand = Vector2(0, 0)
        self.attackCommand = False
        self.measureCommand = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # movement keys
                elif event.key in {pygame.K_RIGHT, pygame.K_d}:
                    self.movePlayerCommand.x = 1
                elif event.key in {pygame.K_LEFT, pygame.K_a}:
                    self.movePlayerCommand.x = -1
                elif event.key in {pygame.K_DOWN, pygame.K_s}:
                    self.movePlayerCommand.y = 1
                elif event.key in {pygame.K_UP, pygame.K_w}:
                    self.movePlayerCommand.y = -1
                # attack key
                elif event.key == pygame.K_SPACE:
                    self.attackCommand = True
                elif event.key == pygame.K_x:
                    self.measureCommand = True

        return True
