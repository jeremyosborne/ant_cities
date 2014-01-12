import time
from entities.entity import Entity



class Leaf(Entity):
    """Capture and convert to energy.
    """
    name = "leaf"
    
    def __init__(self, world):
        
        Entity.__init__(self, world)
        
        # Leaves disappear after a certain number of seconds.
        self.c.add("age", lifespan=120)
        
    def process(self, time_passed):
        Entity.process(self, time_passed)
        if self.c["age"].old:
            self.flags.add("dead")
