from entities.components.component import Component
from commonmath import mmval

class Energy(Component):
    """Simple view of metabolic resource of an entity.
    """
    
    _cname = "energy"
    
    def __init__(self, maximum=1000, current=None, burn_rate=0):
        """Set up initial health of the entity.
        """
        # Total amount of energy we can have.
        self.max = maximum
        # Default is maximum unless current is set to something other than None.
        self._current = current if current != None else maximum
        # Delta per second.
        self.burn_rate = burn_rate
        # Minimum amount of energy before we're considered empty?
        self.min = 0

    def process(self, time_passed):
        """Being alive costs energy.
        """
        self.current -= self.burn_rate*time_passed
        
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        # Boundary check.
        self._current = mmval(self.max, self._current+value, self.min)
        
    @property
    def empty(self):
        """Are our gas tanks empty?
        """
        return True if self.current <= self.min else False
