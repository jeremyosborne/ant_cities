from entities.components.component import Component

class Energy(Component):
    """Simple view of metabolic resource of an entity.
    """
    
    name = "energy"
    
    def __init__(self, maximum=1000):
        """Set up initial health of the entity.
        """
        self.max = maximum
        self.current = maximum
        # Delta per second.
        self.metabolic_burn_rate = 10
        # Minimum amount of energy before we're considered empty?
        self.min = 0

    def process(self, time_passed):
        """Being alive costs energy.
        """
        self.current -= self.metabolic_burn_rate*time_passed

    @property
    def empty(self):
        """Are our gas tanks empty?
        """
        return True if self.current <= self.min else False
