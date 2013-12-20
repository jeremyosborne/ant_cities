import pygame
import statemachines
from entities.gameentity import GameEntity


class Ant(GameEntity):
    
    def __init__(self, world, image, base, color):
        
        GameEntity.__init__(self, world, "ant", image)
        
        exploring_state = statemachines.AntStateExploring(self)
        seeking_state = statemachines.AntStateSeeking(self)
        delivering_state = statemachines.AntStateDelivering(self)
        energy_depleted_state = statemachines.AntStateEnergyDepleted(self)
        powerup_state = statemachines.AntStatePowerUp(self)

        self.color = color
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
        
        self.carry_image = None
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, world):
        #Question for Jeremy stop position
        if self.carry_image:
            self.carry_image = None
            #We need to tell the base that an item has arrived.
            self.base.increment_leaf()
        
    def process(self, time_passed):
        
        #Process energy consumption
        self.energy_current = self.energy_current - ((time_passed) * self.energy_consumption_per_second)
        #Is ant energy so low that we need to dump health into energy?
        if self.energy_current <= self.health_to_energy_needed:
            self.energy_current += self.health_to_energy_conversion_value
            self.health_current -= self.health_to_energy_conversion_cost
            
        #Should the ant die?
        if self.energy_current < self.energy_death or self.health_current <= self.health_death:
            self.world.remove_entity(self)
        else:
            GameEntity.process(self, time_passed)
    
    def delete(self):
        # Update team stats.
        self.base.ant_count -= 1
        self.base.ant_dead += 1
        
        