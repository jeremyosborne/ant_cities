import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

import statemachines
import global_data
import screen_entity


class GameEntity(object):
    
    def __init__(self, world, name, image):
        
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        
        self.brain = statemachines.StateMachine()
        
        self.id = 0
        
    def render(self, viewport):
        
        x, y = self.location
      
        #Let's call the viewport entity render.  It will determine if it's on screen.
       
        viewport.render_entity(self.image, x, y)
        
        #render mini-map
        #map is 256 across and 192 down
#       minimap_x = x/4. + 750
#       minimap_y = y/4. + 550
        #surface.set_at((int(minimap_x), int(minimap_y)), self.color)
#        pygame.draw.rect(surface, self.color, (int(minimap_x), int(minimap_y), 4, 4))   
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.speed > 0. and self.location != self.destination:
            
            vec_to_destination = self.destination - self.location        
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading
            
class Base (GameEntity):
    def __init__(self, world, image, base_id, color):
        GameEntity.__init__(self, world, "base", image)

        self.base_id = base_id  #Not used yet and may never be.
        self.leaves = 0
        self.leaves_returned = 0
        self.leaves_mulching = 0
        self.food_units = 5
        self.color = color 
        
    def increment_leaf(self):
        self.leaves += 1
        self.leaves_returned += 1
         
    def process(self, time_passed):
        if self.leaves > 100:
            self.leaves -= 100
            self.food_units += 10
    
        
class Leaf(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "leaf", image)
        self.color = (0, 255, 0)
        

class Ant(GameEntity):
    
    def __init__(self, world, image, base, color):
        
        GameEntity.__init__(self, world, "ant", image)

     
        exploring_state = statemachines.AntStateExploring(self)
        seeking_state = statemachines.AntStateSeeking(self)
        delivering_state = statemachines.AntStateDelivering(self)
        hunting_state = statemachines.AntStateHunting(self)
        hungry_state = statemachines.AntStateHungry(self)
        eating_state = statemachines.AntStateEating(self)

        self.color = color
        self.base = base
        self.base_location = base.location        
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)
        self.brain.add_state(hungry_state)
        self.brain.add_state(eating_state)
        
        self.hunger = 1000.
        
        self.carry_image = None
        
        self.bar_surface = pygame.surface.Surface((25, 4)).convert()
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, world):
        
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            # surface.blit(self.carry_image, (x-w, y-h/2))  #Let's not draw the leaf on the background when dropped.
            self.carry_image = None
            #We need to tell the base that an item has arrived.
            self.base.increment_leaf()
            
        
    def render(self, viewport):
        
        x, y = self.location
        w, h = self.image.get_size()
        
        #Let's draw the ant first.
        viewport.render_entity(self.image, x-w, y-h/2)
        
        #If it's carrying a leaf, let's draw that too.
        if self.carry_image:
            w, h = self.carry_image.get_size()
            viewport.render_entity(self.carry_image, x-w, y-h/2)
        
        #Hunger Bar.  Draw the inital bar.
        self.bar_surface.fill( (255, 0, 0), (0, 0, 25, 4))
        #Now draw how much food is left over the inital bar
        self.bar_surface.fill( (0, 255, 0), (0, 0, self.hunger/40, 4))
        viewport.render_entity(self.bar_surface, x-30, y+10)

    def process(self, time_passed):
        self.hunger -= 1
        GameEntity.process(self, time_passed)
        
