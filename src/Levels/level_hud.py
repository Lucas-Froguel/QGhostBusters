import time

import pygame
from pygame.sprite import Sprite
from pygame import Vector2, Rect, Surface
from pygame.image import load
from pygame.transform import scale
from src.Units.player import Player


class BaseLevelHud:
    def __init__(self, cellSize: Vector2 = None, player: Player = None):
        self.cellSize = cellSize
        self.player_data_hud = PlayerDataHUD(player=player, cellSize=self.cellSize)

    def update(self):
        self.player_data_hud.update()


class PlayerDataHUD:
    def __init__(self, player: Player = None, cellSize: Vector2 = None):
        self.player = player
        self.cellSize = cellSize

        self.hearts: [LifeHeart] = [
            LifeHeart(cellSize=self.cellSize, position=Vector2(life, 0))
            for life in range(player.max_health)
        ]
        self.measure_timer: MeasureTimer = MeasureTimer(
            last_measure_time=self.player.last_measure_time,
            min_measure_time=self.player.min_measure_time,
        )

        self.update()

    def update_health(self):
        for life in range(self.player.max_health):
            if life < self.player.health:
                self.hearts[life].update(has_health=True)
            else:
                self.hearts[life].update(has_health=False)

    def update_measure_timer(self):
        self.measure_timer.update(
            last_measure_time=self.player.last_measure_time,
            min_measure_time=self.player.min_measure_time,
        )

    def update(self):
        self.update_health()
        if self.measure_timer:
            self.update_measure_timer()


class MeasureTimer:
    def __init__(self, last_measure_time: int = 0, min_measure_time: int = 0):
        self.last_measure_time = last_measure_time
        self.min_measure_time = min_measure_time
        self.time_to_wait = 0
        self.measure_timer_font = pygame.font.SysFont("fonts/Baskic8.otf", 30)
        self.measure_timer: Surface = None

    def update(self, last_measure_time: int = 0, min_measure_time: int = 0):
        self.last_measure_time = last_measure_time
        self.min_measure_time = min_measure_time
        time_waited = int(time.time() - self.last_measure_time)
        self.time_to_wait = (
            self.min_measure_time - time_waited
            if time_waited < self.min_measure_time
            else 0
        )

    def render(self):
        self.measure_timer = self.measure_timer_font.render(
            f"Measure time:{self.time_to_wait}", False, (255, 0, 0)
        )


class LifeHeart(Sprite):
    def __init__(self, position: Vector2 = None, cellSize: Vector2 = None):
        super().__init__()
        self.full_heart_image = load("src/Levels/sprites/life_heart_full.png")
        self.full_heart_image = scale(self.full_heart_image, cellSize)
        self.empty_heart_image = load("src/Levels/sprites/life_heart_empty.png")
        self.empty_heart_image = scale(self.empty_heart_image, cellSize)
        self.image = self.full_heart_image
        self.has_health = True
        self.rect = Rect(
            position.x * cellSize.x,
            position.y * cellSize.y,
            cellSize.x,
            cellSize.y,
        )

    def update(self, has_health: bool = True) -> None:
        self.has_health = has_health
        self.image = (
            self.full_heart_image if self.has_health else self.empty_heart_image
        )
