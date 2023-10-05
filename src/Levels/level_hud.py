import time

import pygame
from pygame import Vector2, Rect, Surface
from pygame.image import load
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

        self.hearts: [FullHeart, EmptyHeart] = []
        self.measure_timer: MeasureTimer = MeasureTimer(
            last_measure_time=self.player.last_measure_time,
            min_measure_time=self.player.min_measure_time
        )

    def update_health(self):
        hearts = []
        for life in range(self.player.max_health):
            if life <= self.player.health:
                hearts.append(FullHeart(cellSize=self.cellSize, position=Vector2(life, 1)))
            else:
                hearts.append(EmptyHeart(cellSize=self.cellSize, position=Vector2(life, 1)))
        self.hearts = hearts

    def update_measure_timer(self):
        self.measure_timer.update(
            last_measure_time=self.player.last_measure_time,
            min_measure_time=self.player.min_measure_time
        )

    def update(self):
        self.update_health()
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
        self.time_to_wait = self.min_measure_time - time_waited if time_waited < self.min_measure_time else 0

    def render(self):
        self.measure_timer = self.measure_timer_font.render(
            f"Measure time:{self.time_to_wait}", False, (255, 0, 0)
        )


class FullHeart:
    def __init__(self, position: Vector2 = None, cellSize: Vector2 = None):
        self.image = load("src/Levels/sprites/life_heart_full.png")
        self.rect = Rect(
            position.x * cellSize.x,
            position.y * cellSize.y,
            cellSize.x,
            cellSize.y,
        )


class EmptyHeart:
    def __init__(self, position: Vector2 = None, cellSize: Vector2 = None):
        self.image = load("src/Levels/sprites/life_heart_empty.png")
        self.rect = Rect(
            position.x * cellSize.x,
            position.y * cellSize.y,
            cellSize.x,
            cellSize.y,
        )
