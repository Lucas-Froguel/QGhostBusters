import pygame

from src.game_state import GameState

game = GameState()
game.run()

pygame.mixer.music.stop()
pygame.quit()
