from entities.components.component import Component
from commonmath import mmval

class Health(Component):
    """Simple view of the life of an entity via a number.
    When number reaches zero, it is assumed entity is in some state of death.
    """
    
    _cname = "health"
    
    def __init__(self, maximum=100):
        """Set up initial health of the entity.
        """
        self.max = maximum
        self._current = maximum
        self.min = 0

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        # Boundary check.
        self._current = mmval(self.max, self._current+value, self.min)

    @property
    def dead(self):
        """Are we dead according to our health?
        """
        return True if self.current <= self.min else False
