import time
from entities.gameentity import GameEntity



class Leaf(GameEntity):
    def __init__(self, world):
        GameEntity.__init__(self, world, "leaf")
        
    def process(self, time_passed):
        # Die after 2 minutes.  
        # If an ant has already grabbed it, it's already out of the game world.
        if time.time() - self.born_time > 120.:
            self.world.remove_entity(self)
            #print "Removing leaf from game world."
