class Trap:
    def __init__(self, x, y, damage=1, visible=True):
        self.x = x
        self.y = y
        self.damage = damage
        self.visible = visible

    def activate(self, player):
        player.health -= self.damage

    def set_position(self, x, y):
        self.x = x
        self.y = y
