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
        self.base.ant_count += 1
        self.base.ant_born += 1
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
        self.energy_full = 1000.
        self.energy_current = self.energy_full
        self.energy_consumption_per_second = 10.
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
        
        self.energy_bar_surface = pygame.surface.Surface((25, 4)).convert()
        self.health_bar_surface = pygame.surface.Surface((25, 4)).convert()
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, world):
        #Question for Jeremy stop position
        if self.carry_image:
            self.carry_image = None
            #We need to tell the base that an item has arrived.
            self.base.increment_leaf()
        
    def render(self, viewport):
        
        x, y = self.location
        w, h = self.image.get_size()
        
        #Let's draw the ant first.
        image = pygame.transform.rotate(self.image, self.direction*-1.)
        viewport.render_entity(image, x, y, self)

        #If it's in an appropriate zoom level, draw the leaf and the energy bar.
        if viewport.current_zoom_level < 6:     
            #If it's carrying a leaf, let's draw that too.
            if self.carry_image:
                #w, h = self.carry_image.get_size()
                image = pygame.transform.rotate(self.carry_image, self.direction*-1.)
                w, h = self.image.get_size()
                viewport.render_entity(image, x, y, self)
        
            #Energy and Health Bar.  Draw the inital bar.
            self.energy_bar_surface.fill( (255, 0, 0), (0, 0, 25, 4))
            self.health_bar_surface.fill( (255, 0, 0), (0, 0, 25, 4))
            #Now draw how much energy is left over the inital bar and health
            self.energy_bar_surface.fill( (0, 255, 0), (0, 0, self.energy_current/40, 4))
            viewport.render_entity(self.energy_bar_surface, x, y+20, self)
            self.health_bar_surface.fill( (0, 255, 0), (0, 0, self.health_current/4, 4))
            viewport.render_entity(self.health_bar_surface, x, y+25, self)

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
        self.base.ant_count -= 1
        self.base.ant_dead += 1
        
        