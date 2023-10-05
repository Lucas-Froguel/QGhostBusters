from pygame.sprite import Sprite, Group


class BaseGhost(Sprite):
    def __int__(self):
        pass

    def move(self):
        pass

    def collapse(self):
        pass

    def leave_trap(self):
        pass


class EasyGhost(BaseGhost):
    pass


class GhostGroup(Group):
    pass
