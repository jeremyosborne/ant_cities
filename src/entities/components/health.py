from entities.components.component import Component
from commonmath import mmval

class Health(Component):
    """Simple view of the life of an entity via a number.
    When number reaches zero, it is assumed entity is in some state of death.
    """
    
    _cname = "health"
    
    # Default value for property computation.
    _val = 0
    
    doprocess = False
    
    def __init__(self, maximum=100):
        """Set up initial health of the entity.
        
        maximum {number} Sets the current and maximum health value.
        """
        self.max = maximum
        self.min = 0
        self.val = maximum

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        # Boundary check.
        self._val = mmval(self.max, value, self.min)

    @property
    def dead(self):
        """Are we dead according to our health?
        """
        return True if self.val <= self.min else False
