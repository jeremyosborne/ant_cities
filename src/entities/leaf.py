import time
from entities.entity import Entity



class Leaf(Entity):
    
    name = "leaf"
    
    def __init__(self, world):
        
        Entity.__init__(self, world)
        
        # Leaves have a max lifespan of 120 seconds.
        self.add_component("age", lifespan=120)
        
    def process(self, time_passed):
        Entity.process(self, time_passed)
        if self.components["age"].old:
            self.world.remove_entity(self)
