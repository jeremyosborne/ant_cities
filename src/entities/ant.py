import pygame
import statemachines
from entities.gameentity import GameEntity


class Ant(GameEntity):
    
    def __init__(self, world, image, base, color):
        
        GameEntity.__init__(self, world, "ant", image)
     
        exploring_state = statemachines.AntStateExploring(self)
        seeking_state = statemachines.AntStateSeeking(self)
        delivering_state = statemachines.AntStateDelivering(self)
        hungry_state = statemachines.AntStateHungry(self)
        eating_state = statemachines.AntStateEating(self)

        self.color = color
        self.base = base
        self.base_location = base.location        
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hungry_state)
        self.brain.add_state(eating_state)
        
        #Following attributes exist in base class, values specific to our ants.
        self.speed_up_acceleration = 30.
        self.slow_down_acceleration = -50.
        self.max_speed = 120.
        self.rotation_per_second = 90.
        
        self.hunger = 1000.
        self.food_consumption_per_second = 10.
        
        self.carry_image = None
        
        self.bar_surface = pygame.surface.Surface((25, 4)).convert()
        
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

        #If it's in an appropriate zoom level, draw the leaf and the food bar.
        if viewport.current_zoom_level < 6:     
            #If it's carrying a leaf, let's draw that too.
            if self.carry_image:
                #w, h = self.carry_image.get_size()
                image = pygame.transform.rotate(self.carry_image, self.direction*-1.)
                w, h = self.image.get_size()
                viewport.render_entity(image, x, y, self)
        
            #Hunger Bar.  Draw the inital bar.
            self.bar_surface.fill( (255, 0, 0), (0, 0, 25, 4))
            #Now draw how much food is left over the inital bar
            self.bar_surface.fill( (0, 255, 0), (0, 0, self.hunger/40, 4))
            viewport.render_entity(self.bar_surface, x, y+20, self)

    def process(self, time_passed):
        
        #Process food consumption
        self.hunger = self.hunger - ((time_passed) * self.food_consumption_per_second)
        GameEntity.process(self, time_passed)