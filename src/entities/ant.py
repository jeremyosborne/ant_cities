from entities.entity import Entity
import entities.ai.ants as antbrainstates

class Ant(Entity):
    
    name = "ant"
    
    def __init__(self, world, base):
        
        Entity.__init__(self, world)
                
        self.brain.add_state(antbrainstates.Exploring())
        self.brain.add_state(antbrainstates.Seeking())
        self.brain.add_state(antbrainstates.Delivering())
        self.brain.add_state(antbrainstates.EnergyDepleted())
        self.brain.add_state(antbrainstates.PowerUp())
        # Default state.
        self.brain.set_state("exploring")
        
        self.c.add("health")
        self.c.add("energy", burn_rate=2.)
        
        self.c.add("facing")
        self.c.add("velocity", max_speed=120., acceleration=30., rotation_speed=180.)
        self.c.add("destination")

        # {Entity} What is our home base.
        self.base = base
        
        # {Entity|None} Ants can carry a single entity (that is likely a leaf).
        self.inventory = None

    @property
    def team_id(self):
        """What team are we on?
        """
        return self.base.c["team"].id

    def carry(self, entity):
        """Ant picks up the entity and takes possession of it.
        """
        # Remove the entity from the world.
        # TODO: Should make this transactional and prevent attempting to
        # remove things that don't exist in the world. (Perhaps remove_entity
        # should remove the entity being removed, or return none?)
        self.world.remove_entity(entity)
        self.inventory = entity
        
    def drop(self):
        """Drop a particular item, assumed to only be called at the base.
        """
        if self.inventory:
            self.base.add_resource(self.inventory)
            self.inventory = None
        
    def process(self, time_passed):
        Entity.process(self, time_passed)

        energy = self.c["energy"]
        health = self.c["health"]
        
        # Is ant energy so low that we need to dump health into energy?
        if energy.empty:
            energy.val += 100
            health.val -= 10
        
        # Heading matches course of velocity.
        self.c["facing"].set(self.c["velocity"].course)
        
        # Should the ant die?
        if health.dead:
            self.world.remove_entity(self)
    
    def delete(self):
        # Update team stats.
        Entity.delete(self)
        self.base.c["team"].stats[self.name] -= 1
        self.base.c["team"].stats[self.name+"-removed"] += 1
