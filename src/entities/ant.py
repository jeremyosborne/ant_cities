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
        
        self.add_component("health")
        self.add_component("energy", burn_rate=10)
        
        self.add_component("facing")
        self.add_component("velocity", max_speed=120., acceleration=30., rotation_speed=720.)
        self.add_component("destination")

        # {Entity} What is our home base.
        self.base = base
        
        # {Entity|None} Ants can carry a single entity (that is likely a leaf).
        self.inventory = None

    @property
    def team_id(self):
        """What team are we on?
        """
        return self.base.components["team"].id

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
            self.inventory = None
            # Assume right now that the ant is carrying a leaf.
            self.base.increment_leaf()
        
    def process(self, time_passed):
        Entity.process(self, time_passed)

        energy = self.components["energy"]
        health = self.components["health"]
        
        # Is ant energy so low that we need to dump health into energy?
        if energy.empty:
            energy.val += 100
            health.val -= 10
        
        # Heading matches course of velocity.
        self.components["facing"].set(self.components["velocity"].course)
        
        # Should the ant die?
        if health.dead:
            self.world.remove_entity(self)
    
    def delete(self):
        # Update team stats.
        Entity.delete(self)
        self.base.components["team"].stats[self.name] -= 1
        self.base.components["team"].stats[self.name+"-removed"] += 1
