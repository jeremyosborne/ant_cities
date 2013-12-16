from entities.gameentity import GameEntity



class Base (GameEntity):
    def __init__(self, world, image, base_id, color, description):
        GameEntity.__init__(self, world, "base", image)

        self.base_id = base_id  #Not used yet and may never be.
        self.leaves = 0
        self.leaves_returned = 0  #Total number of leaves returned since start.
        self.leaves_mulching = 0
        self.energy_units = 5
        self.color = color # Used on the minimap.
        self.ant_count = 0
        self.ant_born = 0
        self.ant_dead = 0
        self.world.base_count += 1
        self.description = description
         
    def process(self, time_passed):
        if self.leaves > 100:
            self.leaves -= 100
            self.energy_units += 10
            
    def increment_leaf(self):
        self.leaves += 1
        self.leaves_returned += 1
                    
    def delete(self):
        self.world.base_count -= 1
