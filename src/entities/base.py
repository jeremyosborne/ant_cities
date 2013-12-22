from entities.entity import Entity
from entities.ant import Ant


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
        
        # Radial size of the nest from location attribute.
        # Hackish: allows ants to drop things back at the base.
        self.size = 5.
         
    def process(self, time_passed):
        if self.leaves > 100:
            self.leaves -= 100
            self.energy_units += 10
            
    def increment_leaf(self):
        self.leaves += 1
        self.leaves_returned += 1

    def create_entity(self, name, placement_offset=(0, 0)):
        """Create an entity and place it under our control.
        
        [placement_offset] {tuple} (x, y) offset relative to starting location
        on top of base.
        
        returns the entity.
        """
        # Right now, we only create ants.
        entity = None
        if name == "ant":
            entity = Ant(self.world, self)
            self.ant_count += 1
            self.ant_born += 1
            basex, basey = self.location
            offsetx, offsety = placement_offset
            entity.location = (basex+offsetx, basey+offsety)
            entity.brain.set_state("exploring")
        else:
            assert False, "%s name is not acceptable for creating." % name
        
        return entity

    @property
    def team(self):
        """What team are we on?
        """
        return self._team_id

    def __str__(self):
        return "Base of %s" % self._team_name
