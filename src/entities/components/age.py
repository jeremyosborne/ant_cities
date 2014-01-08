from entities.components.component import Component
import time

class Age(Component):
    """Tracks the age of an entity in elapsed game time.
    """
    
    _cname = "age"
    
    def __init__(self, lifespan=float('inf')):
        """Set up age constraints.
        
        lifespan {number} How many seconds should the lifespan of this entity
        be?
        """
        # Always count relative to ourselves.
        self.val = 0
        
        # How long should we live?
        # Not called max because implementations might treat lifespan differently.
        self.lifespan = lifespan

    def process(self, time_passed):
        # Only age when the game runs.
        self.val += time_passed

    @property
    def old(self):
        """Have we passed the expected lifespan?
        """
        return True if self.val >= self.lifespan else False
    