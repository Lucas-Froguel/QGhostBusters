import pygame
from pygame import Vector2
from pygame.sprite import RenderUpdates, GroupSingle

from src.Units.player import Player
from src.Units.ghosts import QGhost


class GameState:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        # window variables
        self.worldSize = None
        self.unitsTexture = None
        self.window = None

        # level variables
        self.level = None
        self.cellSize = Vector2(16, 16)

        self.setup_game_window()

        # player and ghosts
        self._player = Player(cellSize=self.cellSize, worldSize=self.worldSize, position=Vector2(5, 4))
        self.player_group = GroupSingle()
        self.player_group.add(self._player)

        self.ghosts_group = [
            QGhost(cellSize=self.cellSize, worldSize=self.worldSize, position=Vector2(30, 30)),
            QGhost(cellSize=self.cellSize, worldSize=self.worldSize, position=Vector2(70, 10)),
        ]
        self.visible_ghosts_group = RenderUpdates()
        # not good, because if more visible ghosts appear, they won't be here, think more
        self.visible_ghosts_group.add([ghost.visible_parts for ghost in self.ghosts_group])

        self.user_interface = UserInterface()

    def setup_game_window(self):
        # Rendering properties
        self.worldSize = Vector2(80, 40)  # should depend on the map, we need to make this receive variables

        # Window
        windowSize = self.cellSize.elementwise() * self.worldSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption("QhostBusters")

    def update(self,):
        if not self.ghosts_group:
            self.running = False

        self.player_group.update(self.user_interface.movePlayerCommand)
        self.player_group.sprite.attack = self.user_interface.attackCommand
        self.visible_ghosts_group.update()

    def render(self):
        self.window.fill((0, 0, 0))

        self.player_group.draw(self.window)
        self.visible_ghosts_group.draw(self.window)

        pygame.display.update()

    def run(self):
        while self.running:
            self.running = self.user_interface.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


class UserInterface:
    def __init__(self):
        self.movePlayerCommand = Vector2(0, 0)
        self.attackCommand = False

    def processInput(self):
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
