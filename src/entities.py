import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

import statemachines
import global_data


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
        
    def render(self, surface):
        
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))
        
        #render mini-map
        #map is 256 across and 192 down
        minimap_x = x/4. + 750
        minimap_y = y/4. + 550
        #surface.set_at((int(minimap_x), int(minimap_y)), self.color)
        pygame.draw.rect(surface, self.color, (int(minimap_x), int(minimap_y), 4, 4))   
        
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
        
class Spider(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "spider", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.speed = 50. + randint(-20, 20)
        self.color = (128,128,128)
        
    def bitten(self):
        
        self.health -= 1
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image
        self.speed = 140.
        
    def render(self, surface):
        
        GameEntity.render(self, surface)
                
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill( (0, 255, 0), (bar_x, bar_y, self.health, 4))
        
    def process(self, time_passed):
        
        x, y = self.location
        if x > global_data.WORLD_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        
        GameEntity.process(self, time_passed)
        
        
class Sri(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "sri", image)
        self.font = pygame.font.SysFont("arial", 24);
        self.state = "Moving"
        self.time = 0
        self.speed = 50. + randint(-20, 20)
        self.color = (128,128,128)
        self.location = (512, -50)
        self.destination = Vector2(512, 128)

        
    def render(self, surface):
        
        GameEntity.render(self, surface)
        
        if self.state == "Yell":     
            x, y = self.location
            label = self.font.render("Seth!", True, (0, 0, 0))
            surface.blit(label, (x-30, y-50))
        if self.state == "Bloody":
            x, y = self.location
            label = self.font.render("Bloody Hell!", True, (0, 0, 0))
            surface.blit(label, (x-60, y-50))
        
    def process(self, time_passed):
        
        x, y = self.location
        if x > global_data.WORLD_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        if y == 128:
            if self.time == 0:
                self.state = "Wait to Yell"
            self.time += 25
            if self.time == 1000:
                self.state = "Yell"
                self.world.add_sri()
            if self.time == 5000:
                self.state= "Bloody"
            if self.time == 8000:
                self.destination = Vector2(512, -2048)
            
        GameEntity.process(self, time_passed)

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
            
        
    def render(self, surface):
        
        GameEntity.render(self, surface)
        
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))

        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill( (0, 255, 0), (bar_x, bar_y, self.hunger/40, 4))

    def process(self, time_passed):
        self.hunger -= 1
        GameEntity.process(self, time_passed)
        
                        
class Seth(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "seth", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 100
        self.speed = 50. + randint(-20, 20)
        self.hungry = 1000
        self.panic = 0
        self.font = pygame.font.SysFont("arial", 16);
        
        exploring_state = statemachines.SethStateExploring(self)
        seeking_state = statemachines.SethStateSeeking(self)
        eating_state = statemachines.SethStateEating(self)
        panic_state = statemachines.SethStatePanic(self)
        running_state = statemachines.SethStateRunning(self)
        
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(eating_state)
        self.brain.add_state(panic_state)
        self.brain.add_state(running_state)
        
        self.color = (230, 230, 230)
        
        
    def bitten(self):
        
        self.health -= 1
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image
        self.speed = 140.
        
    def render(self, surface):
        
        GameEntity.render(self, surface)
        
        if self.hungry < 1000 and self.panic == 0:
            x, y = self.location
            label = self.font.render("YUM!", True, (0, 0, 0))
            surface.blit(label, (x, y+20))
            
        if self.panic > 0 and self.panic < 1000:
            x, y = self.location
            label = self.font.render("OH NO!", True, (0, 0, 0))
            surface.blit(label, (x-30, y-35))
            
        if self.panic == 1000:
            x, y = self.location
            label = self.font.render("RUN!", True, (0, 0, 0))
            surface.blit(label, (x-20, y-40))
                    
        #x, y = self.location
        #w, h = self.image.get_size()
        #bar_x = x - 12
        #bar_y = y + h/2
        #surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        #surface.fill( (0, 255, 0), (bar_x, bar_y, self.health, 4))
        
    def process(self, time_passed):
        
        x, y = self.location
        if x > global_data.WORLD_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        
        GameEntity.process(self, time_passed)