from entities.gameentity import GameEntity



class Base(GameEntity):
    def __init__(self, world, image, base_id, team_name):
        GameEntity.__init__(self, world, "base", image)

        self.base_id = base_id
        self.leaves = 0
        self.leaves_returned = 0  #Total number of leaves returned since start.
        self.leaves_mulching = 0
        self.energy_units = 5
        self.ant_count = 0
        self.ant_born = 0
        self.ant_dead = 0

        self._team_name = team_name
         
    def process(self, time_passed):
        if self.leaves > 100:
            self.leaves -= 100
            self.energy_units += 10
            
    def increment_leaf(self):
        self.leaves += 1
        self.leaves_returned += 1

    @property
    def team(self):
        """What team are we on?
        """
        return self.base_id

    def __str__(self):
        return "Base of %s" % self._team_name
