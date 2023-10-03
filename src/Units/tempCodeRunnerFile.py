from pygame import Vector2, Rect
from pygame.sprite import Sprite
from pygame.transform import rotate


class BaseUnit(Sprite):
    def move(self):
        pass

    def attack(self):
        pass