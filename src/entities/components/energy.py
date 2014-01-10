from entities.components.component import Component
from commonmath import mmval

class Energy(Component):
    """Simple view of metabolic resource of an entity.
    """
    
    _cname = "energy"

    # Default value for property computation.
    _val = 0.
    
    def __init__(self, maximum=100., val=None, burn_rate=0.):
        """Set up initial health of the entity.
        """
        # Total amount of energy we can have.
        self.max = maximum
        # Minimum amount of energy before we're considered empty?
        self.min = 0.
        # Default is maximum unless val is set to something other than None.
        self.val = val if val != None else maximum
        # Delta per second.
        self.burn_rate = burn_rate
        
    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        # Boundary check.
        self._val = mmval(self.max, value, self.min)
        
    @property
    def empty(self):
        """Are our gas tanks empty?
        """
        return True if self.val <= self.min else False

    def process(self, time_passed):
        """It is assumed that just being alive costs energy.
        """
        print "Before:", self.val
        self.val -= self.burn_rate*time_passed
        print "After:", self.val
        