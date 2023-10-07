from src.user_interfaces import MessageUserInterface
from pygame.sprite import Sprite
from pygame import Vector2, Rect, font

font.init()
my_font = font.SysFont("fonts/Baskic8.otf", 36)


class BaseMessage(Sprite):
    def __init__(self, worldSize, cellSize, text: str = None, position=None):
        super().__init__()
        if position is None:
            self.position = Vector2(
                worldSize.x // 4 * cellSize.x, worldSize.y // 4 * cellSize.y
            )
        else:
            self.position = Vector2(position.x * cellSize.x, position.y * cellSize.y)
        self.image = my_font.render(text, 0, "red", "black")
        self.rect = Rect(
            self.position.x,
            self.position.y,
            worldSize.x // 2,
            worldSize.y // 2,
        )

        self.user_interface = MessageUserInterface()
        self.text = text
        self.show = True

    def update(self):
        self.show = self.user_interface.process_input()
