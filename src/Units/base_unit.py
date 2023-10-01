from pygame import Vector2, Rect
from pygame.sprite import Sprite


class BaseUnit(Sprite):
    def move(self):
        pass

    def attack(self):
        pass

    def heal(self):
        pass

    def lay_trap(self):
        pass


class Unit(BaseUnit):
    """
    Base class for player and ghosts.
    """

    def __init__(self, cellSize: Vector2 = None, worldSize: Vector2 = None, position: Vector2 = None):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param position: position on the map (in units of cells)
        """
        super().__init__()
        self.cellSize = cellSize
        self.worldSize = worldSize
        self.position = position
        self.image = None
        self.rect = Rect(
            self.position.x * self.cellSize.x,
            self.position.y * self.cellSize.y,
            self.cellSize.x,
            self.cellSize.y
        )

    def move(self, moveVector: Vector2) -> None:
        newUnitPos = self.position + moveVector
        self.position = newUnitPos
        self.rect = self.rect.move(
            self.position.x * self.cellSize.x - self.rect.x,
            self.position.y * self.cellSize.y - self.rect.y,
        )

    def is_unit_in_map(self) -> bool:
        if (
            self.rect.x < 0
            or self.rect.right > self.worldSize.x * self.cellSize.x
            or self.rect.y < 0
            or self.rect.bottom > self.worldSize.y * self.cellSize.y
        ):
            return False
        return True

    def update(self, moveVector: Vector2) -> None:
        if not moveVector:
            return None
        self.move(moveVector=moveVector)
        if not self.is_unit_in_map():
            self.move(moveVector=-moveVector)
