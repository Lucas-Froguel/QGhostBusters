import numpy as np
import pygame
from pygame import Vector2, Rect

from src.Units.units import Ghost, Player

GHOST_SPEED = 0.1


class GameState:
    def __init__(self):
        self.worldSize = Vector2(16, 10)
        self.player = Player(self, Vector2(5, 4))
        self.units = [
            Ghost(self, Vector2(10, 3)),
            Ghost(self, Vector2(10, 5)),
        ]

    def update(self, movePlayerCommand):
        self.player.move(movePlayerCommand)
        for unit in self.units:
            x = GHOST_SPEED * np.random.choice([-1, 0, 1])
            y = GHOST_SPEED * np.random.choice([-1, 0, 1]) if not x else 0
            unit.move(Vector2(x, y))


class UserInterface:
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSize = Vector2(64, 64)
        self.unitsTexture = pygame.image.load("units.png")

        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption("QhostBusters")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.movePlayerCommand = Vector2(0, 0)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.movePlayerCommand = Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.movePlayerCommand.x = 1
                elif event.key == pygame.K_LEFT:
                    self.movePlayerCommand.x = -1
                elif event.key == pygame.K_DOWN:
                    self.movePlayerCommand.y = 1
                elif event.key == pygame.K_UP:
                    self.movePlayerCommand.y = -1

    def update(self):
        self.gameState.update(self.movePlayerCommand)

    def renderUnit(self, unit):
        # Location on screen
        spritePoint = unit.position.elementwise() * self.cellSize

        # Unit texture
        texturePoint = unit.tile.elementwise() * self.cellSize
        textureRect = Rect(
            int(texturePoint.x),
            int(texturePoint.y),
            int(self.cellSize.x),
            int(self.cellSize.y),
        )
        self.window.blit(self.unitsTexture, spritePoint, textureRect)

    def render(self):
        self.window.fill((0, 0, 0))
        self.renderUnit(self.gameState.player)
        for unit in self.gameState.units:
            self.renderUnit(unit)

        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
