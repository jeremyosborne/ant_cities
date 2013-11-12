import time
from entities.gameentity import GameEntity



class Leaf(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "leaf", image)
        self.color = (0, 255, 0)
        self.world.leaf_count += 1
        
    def process(self, time_passed):
        
        #Are we older than two minutes?  If a ant has already grabbed it, it's already
        #out of the game world.
        
        if time.time() - self.born_time > 120.:
            self.world.remove_entity(self)
            self.world.leaf_expired += 1
            #print "Removing leaf from game world."
            
    def delete(self):
        self.world.leaf_count -= 1