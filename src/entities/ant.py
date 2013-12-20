import pygame
import statemachines
from entities.entity import Entity


class Ant(Entity):
    
    def __init__(self, world, base):
        
        Entity.__init__(self, "ant", world)
        
        exploring_state = statemachines.AntStateExploring(self)
        seeking_state = statemachines.AntStateSeeking(self)
        delivering_state = statemachines.AntStateDelivering(self)
        energy_depleted_state = statemachines.AntStateEnergyDepleted(self)
        powerup_state = statemachines.AntStatePowerUp(self)

        self.base = base
        self.base_location = base.location
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(energy_depleted_state)
        self.brain.add_state(powerup_state)
        
        #Following attributes exist in base class, values specific to our ants.
        self.speed_up_acceleration = 30.
        self.slow_down_acceleration = -50.
        self.max_speed = 120.
        self.rotation_per_second = 90.
        
        #Related to energy
        self.max_energy = 1000.
        self.energy_current = self.max_energy
        self.energy_consumption_per_second = 10.
        self.energy_recharge_per_second = 1000
        self.energy_recharge_to_energy_conversion_ratio = .2
        self.energy_death = -100.
        
        #Related to health
        self.max_health = 100
        self.health_current = self.max_health
        self.health_heal_rate = 10 #Per second.
        self.energy_to_heal_rate = .1 #Amount of extra energy required to heal
        self.health_death = 0
        self.health_to_energy_needed = 0 #Value of energy where health gets converted to energy.  10 health to 50 energy  
        self.health_to_energy_conversion_value = 50
        self.health_to_energy_conversion_cost = 10
        
        # Right now, ants can cary a single entity.
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
        
        # Process energy consumption
        self.energy_current = self.energy_current - ((time_passed) * self.energy_consumption_per_second)
        # Is ant energy so low that we need to dump health into energy?
        if self.energy_current <= self.health_to_energy_needed:
            self.energy_current += self.health_to_energy_conversion_value
            self.health_current -= self.health_to_energy_conversion_cost
            
        # Should the ant die?
        if self.energy_current < self.energy_death or self.health_current <= self.health_death:
            self.world.remove_entity(self)
        else:
            Entity.process(self, time_passed)
    
    def delete(self):
        # Update team stats.
        self.base.ant_count -= 1
        self.base.ant_dead += 1
        
    @property
    def team(self):
        """What team are we on?
        """
        return self.base.team
