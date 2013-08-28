import pygame, math
from pygame.locals import *

from random import randint, choice

import pymunk
from pymunk.vec2d import Vec2d

import statemachines
import global_data
import viewport


class GameEntity(object):
    
    def __init__(self, world, name, image):
        
        #a way for an entity to get at attributes about the world.
        self.world = world
        self.name = name
        self.image = image
        self.brain = statemachines.StateMachine()
        self.id = 0
        
        #Movement in the game world
        self.location = Vec2d(0., 0.)
        self.destination = Vec2d(0., 0.)
        self.current_heading = Vec2d(1., 0.)
        self.desired_heading = Vec2d(0., 0.)
        self.speed = 0.
        self.acceleration = 0.
        self.speed_up_acceleration = 0.
        self.slow_down_acceleration = 0.
        self.max_speed = 0.
        self.direction = 0.
        self.rotation_per_second = 0.        

    def apply_acceleration(self, time_passed, distance_to_destination):

        #If we're at 0 and location != destination, then we should start moving.
        if (self.location != self.destination) and (self.speed == 0):
            self.speed = 1.
        else:
            #calculate the distance needed to stop.  If the travel distance is greater,
            #then keep going, else start stopping.
            if abs(self.speed / self.slow_down_acceleration) > (distance_to_destination/self.speed):
                #slow down
                self.acceleration = self.slow_down_acceleration
                self.speed += self.acceleration * time_passed
                if self.speed < 0: self.speed = 5
            else:
                #speed up
                self.acceleration = self.speed_up_acceleration
                self.speed += self.acceleration * time_passed
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
                
    def steer(self, angle_between_vectors, time_passed):
        
        #How much we can steer this tick of the clock.
        steer_time_tick = self.rotation_per_second * time_passed

        #Is the angle we must turn less than steer_time_clock?  If so, then
        #we're done, steer the last little bit.        
        if (abs(angle_between_vectors)) < steer_time_tick:
            self.current_heading = self.desired_heading

        else:  # We must steer.
            angle_to_steer = self.rotation_per_second * time_passed
            if angle_between_vectors < 0:
                angle_to_steer *= -1.
            #Do the rotation
            self.current_heading = self.current_heading.rotated_degrees(angle_to_steer).normalized()
                    
    def move(self, time_passed):
        
        self.desired_heading = (self.destination - self.location).normalized()
        angle_between_vectors = self.current_heading.get_angle_degrees_between(self.desired_heading)
        
        #Do we have to change direction?
        if angle_between_vectors != 0.0:
            self.steer(angle_between_vectors, time_passed)    
        
        #Update location.
        vec_to_destination = self.destination - self.location
        distance_to_destination = vec_to_destination.get_length()
        travel_distance = min(distance_to_destination, time_passed * self.speed)
        self.location += travel_distance * self.current_heading
        
        #Apply acceleration forces.
        self.apply_acceleration(time_passed, distance_to_destination)
        
        self.direction = ((math.atan2(self.current_heading.y, self.current_heading.x)*(180/math.pi))+90)

        #print "headings ", self.current_heading, self.desired_heading
        #print "distance to destination:", distance_to_destination
        #print "location: ", self.location
        #print "speed:", self.speed

        
    def render(self, viewport):
        
        x, y = self.location
        #Let's call the viewport entity render.  It will determine if it's on screen.
        w, h =self.image.get_size()
        image = pygame.transform.rotate(self.image, self.direction*-1.)
        viewport.render_entity(image, x, y, self)  
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.speed > 0. and self.location != self.destination:
            self.move(time_passed) 
            
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
        viewport.render_entity(image, x-w, y-h/2)
        
        #If it's carrying a leaf, let's draw that too.
        if self.carry_image:
            #w, h = self.carry_image.get_size()
            image = pygame.transform.rotate(self.carry_image, self.direction*-1.)
            w, h = self.image.get_size()
            viewport.render_entity(image, x-w, y-h/2)
        
        #Hunger Bar.  Draw the inital bar.
        self.bar_surface.fill( (255, 0, 0), (0, 0, 25, 4))
        #Now draw how much food is left over the inital bar
        self.bar_surface.fill( (0, 255, 0), (0, 0, self.hunger/40, 4))
        viewport.render_entity(self.bar_surface, x-30, y+10)

    def process(self, time_passed):
        
        #Process food consumption
        self.hunger = self.hunger - ((time_passed) * self.food_consumption_per_second)
        GameEntity.process(self, time_passed)
        
