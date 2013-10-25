from entities.gameentity import GameEntity



class Base (GameEntity):
    def __init__(self, world, image, base_id, color):
        GameEntity.__init__(self, world, "base", image)

        self.base_id = base_id  #Not used yet and may never be.
        self.leaves = 0
        self.leaves_returned = 0
        self.leaves_mulching = 0
        self.food_units = 5
        self.color = color 
        
    def increment_leaf(self):
        self.leaves += 1
        self.leaves_returned += 1
         
    def process(self, time_passed):
        if self.leaves > 100:
            self.leaves -= 100
            self.food_units += 10