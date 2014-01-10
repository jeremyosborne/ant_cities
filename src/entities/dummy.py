from entities.entity import Entity

class Dummy(Entity):
    """A dummy entity.
    
    Meant for debugging and testing things.
    """
    name = "dummy"
    
    def __init__(self, world):
        Entity.__init__(self, world)
                
    def process(self, time_passed):
        Entity.process(self, time_passed)

        