import pygame
from entities.entity import Entity
import entities.ai.ants as antbehaviors

from entities.components import Health, Energy

class Ant(Entity):
    
    def __init__(self, world, base):
        
        Entity.__init__(self, "ant", world)
        
        self.base = base
        
        self.brain.add_state(antbehaviors.Exploring())
        self.brain.add_state(antbehaviors.Seeking())
        self.brain.add_state(antbehaviors.Delivering())
        self.brain.add_state(antbehaviors.EnergyDepleted())
        self.brain.add_state(antbehaviors.PowerUp())
        # Default state.
        self.brain.set_state("exploring")
        
        self.add_component(Health())
        self.add_component(Energy())

        #Following attributes exist in base class, values specific to our ants.
        self.speed_up_acceleration = 30.
        self.slow_down_acceleration = -50.
        self.max_speed = 120.
        self.rotation_per_second = 90.
        
        # Ants can carry a single entity (that is likely a leaf).
        self.inventory = None
        
    def carry(self, entity):
        """Ant picks up the entity and takes possession of it.
        """
        # Remove the entity from the world.
        # TODO: Should make this transactional and prevent attempting to
        # remove things that don't exist in the world. (Perhaps remove_entity
        # should remove the entity being removed, or return none?)
        self.world.remove_entity(entity)
        self.inventory = entity
        
    def drop(self, world):
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
            # TODO: Have a converter component.
            energy.current += 100
            health.current -= 10
            
        # Should the ant die?
        if health.dead:
            self.world.remove_entity(self)
    
    def delete(self):
        # Update team stats.
        self.base.ant_count -= 1
        self.base.ant_dead += 1
        
    @property
    def team(self):
        """What team are we on?
        """
        return self.base.team
