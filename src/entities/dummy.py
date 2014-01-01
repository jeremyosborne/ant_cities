from entities.entity import Entity

class Dummy(Entity):
    """A dummy entity.
    
    Meant for debugging and testing things.
    """
    name = "dummy"
    
    def __init__(self, world):
        
        Entity.__init__(self, world)
        
        self.add_component("velocity")
        self.add_component("velocityengine", acceleration=10, max_speed=200, rotation_speed=90)
        self.components["velocityengine"].update(speed=200, course=180)
        
    def process(self, time_passed):
        Entity.process(self, time_passed)

        