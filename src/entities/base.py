from entities.entity import Entity



class Base(Entity):
    def __init__(self, world, team_id, team_name):
        Entity.__init__(self, "base", world)

        # Bases represent the team hierarchy.
        self._team_id = team_id
        self._team_name = team_name

        self.leaves = 0
        self.leaves_returned = 0  #Total number of leaves returned since start.
        self.leaves_mulching = 0
        self.energy_units = 5
        self.ant_count = 0
        self.ant_born = 0
        self.ant_dead = 0

         
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
        return self._team_id

    def __str__(self):
        return "Base of %s" % self._team_name
