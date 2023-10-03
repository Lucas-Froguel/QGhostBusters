import pygame
from pygame import Vector2


class BaseUserInterface:
    def process_input(self):
        pass


class MenuUserInterface(BaseUserInterface):
    def __init__(self, current_menu_item: int = None, menu_items: [dict] = None, music=None):
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
                    if self.current_menu_item < len(self.menu_items) - 1:
                        self.current_menu_item += 1
                        self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_UP:
                    if self.current_menu_item > 0:
                        self.current_menu_item -= 1
                        self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_RETURN:
                    self.select = True
        return self.running


class SettingsMenuUserInterface(BaseUserInterface):
    def __init__(self, current_menu_item: int = None, menu_items: [dict] = None, music=None, volume: float = None):
        self.current_menu_item = current_menu_item
        self.menu_items = menu_items
        self.select = False
        self.quit = False
        self.running = True
        self.music = music
        self.volume = volume

    def process_input(self):
        self.select = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.current_menu_item < len(self.menu_items) - 1:
                        self.current_menu_item += 1
                        self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_UP:
                    if self.current_menu_item > 0:
                        self.current_menu_item -= 1
                        self.music.play_select_menu_item_sound()
                elif event.key == pygame.K_LEFT:
                    if self.volume > 0:
                        self.volume -= 5
                elif event.key == pygame.K_RIGHT:
                    if self.volume < 100:
                        self.volume += 5
                elif event.key == pygame.K_RETURN:
                    self.select = True
        return self.running


class GameUserInterface(BaseUserInterface):
    def __init__(self):
        self.movePlayerCommand = Vector2(0, 0)
        self.attackCommand = False

    def process_input(self):
        self.movePlayerCommand = Vector2(0, 0)
        self.attackCommand = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # movement keys
                elif event.key == pygame.K_RIGHT:
                    self.movePlayerCommand.x = 1
                elif event.key == pygame.K_LEFT:
                    self.movePlayerCommand.x = -1
                elif event.key == pygame.K_DOWN:
                    self.movePlayerCommand.y = 1
                elif event.key == pygame.K_UP:
                    self.movePlayerCommand.y = -1
                # attack key
                elif event.key == pygame.K_SPACE:
                    self.attackCommand = True

        return True
