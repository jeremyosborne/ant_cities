from entities.entity import Entity
from entities.ant import Ant


class Anthill(Entity):
    """The anthill of our ants.
    """
    name = "anthill"
    
    body_size = 50.
    
    def __init__(self, world, team_id, team_name):
        
        Entity.__init__(self, world)

        self.c.add("team", id=team_id, name=team_name)
        self.c.add("energy", maximum=1000, val=0)
        self.c.add("inventory")
        
    @property
    def team_id(self):
        """What team are we on?
        """
        return self.c["team"].id
    
    def process(self, time_passed):
        # Process resources.
        inv = self.c["inventory"].carried
        if inv:
            # One item at a time.
            item = inv.pop()
            if item.name == "leaf":
                self.c["energy"].val += 5
    
    def remove_resource(self, resource_name, amount=1):
        """Removes a resource from the base.
        """
        if resource_name == "energy":
            r = min(self.c["energy"].val, amount)
            self.c["energy"].val -= amount
            return r
        else:
            assert "Could not remove resource of name:", resource_name
            

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
            basex, basey = self.location
            offsetx, offsety = placement_offset
            entity.location = (basex+offsetx, basey+offsety)
        else:
            assert False, "%s name is not acceptable for creating." % name
        
        return entity

