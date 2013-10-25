from entities.gameentity import GameEntity



class Leaf(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "leaf", image)
        self.color = (0, 255, 0)