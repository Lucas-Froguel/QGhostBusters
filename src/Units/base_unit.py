from pygame import Vector2, Rect
from pygame.sprite import Sprite
from pygame.mixer import Channel
from src.SoundEffects.sound_manager import BaseSoundManager
from src.Units.utils import load_all_images_in_folder


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

    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
    ):
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
            self.cellSize.y,
        )
        self.channel = channel
        self.sound_manager: BaseSoundManager = None

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

    def update(self, moveVector: Vector2 = None) -> None:
        if not moveVector:
            return None
        self.move(moveVector=moveVector)
        if not self.is_unit_in_map():
            self.move(moveVector=-moveVector)


class AnimatedUnit(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        channel: Channel = None,
        images_folder: str = None,
        images_name: str = None,
    ):
        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        self.images = load_all_images_in_folder(
            folder_path=images_folder, file_name=images_name, cellSize=cellSize
        )
        self.num_images = len(self.images)
        self.current_image_index: int = 0
        self.current_image_direction: int = 1
        self.image = self.images[self.current_image_index]

    def update_image(self):
        self.current_image_index += self.current_image_direction / 2
        if self.current_image_index >= self.num_images - 1:
            self.current_image_direction = -1
            self.current_image_index = self.num_images - 1
        elif self.current_image_direction <= 0:
            self.current_image_direction = +1
            self.current_image_index = 0

        self.image = self.images[int(self.current_image_index)]

    def update(self, moveVector: Vector2 = None):
        super().update(moveVector=moveVector)
        self.update_image()
