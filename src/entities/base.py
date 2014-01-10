from entities.entity import Entity
from entities.ant import Ant


class Base(Entity):
    
    name = "base"
    
    def __init__(self, world, team_id, team_name):
        
        Entity.__init__(self, world)

        self.add_component("team", id=team_id, name=team_name)
        self.add_component("energy", maximum=1000, val=0)
        
        self.leaves = 0
        
        # Radial size of the nest from location attribute.
        # Hackish: allows ants to drop things back at the base.
        self.size = 5.
    
    @property
    def team_id(self):
        """What team are we on?
        """
        return self.components["team"].id
    
    def process(self, time_passed):
        # Process resources.
        if self.leaves:
            self.leaves -= 1
            self.components["energy"].val += 5
    
    def add_resource(self, resource):
        """Add a resource to this base.
        
        resource {Entity} Resource to be added.
        """
        if resource.name == "leaf":
            self.leaves += 1
            self.components["team"].stats["leaves-returned"] += 1

    def remove_resource(self, resource_name, amount=1):
        """Removes a resource from the base.
        """
        if resource_name == "energy":
            r = min(self.components["energy"].val, amount)
            self.components["energy"].val -= amount
            return r
        else:
            assert "Could not remove resource of name:", resource_name
            

    def create_entity(self, name, placement_offset=(0, 0)):
        """Create an entity and place it under our control.
        
        [placement_offset] {tuple} (x, y) offset relative to starting location
        on top of base.
        
        returns the entity.
        """
        team = self.components["team"]
        # Right now, we only create ants.
        entity = None
        if name == "ant":
            entity = Ant(self.world, self)
            team.stats[entity.name] += 1
            team.stats[entity.name+"-added"] += 1
            basex, basey = self.location
            offsetx, offsety = placement_offset
            entity.location = (basex+offsetx, basey+offsety)
        else:
            assert False, "%s name is not acceptable for creating." % name
        
        return entity

