import math
import pygame

from pymunk.vec2d import Vec2d

import statemachines
import appid



class GameEntity(object):

    def __init__(self, world, name, image):
        
        #a way for an entity to get at attributes about the world.
        self.world = world
        self.name = name
        self.image = image
        self.brain = statemachines.StateMachine()
        # Entity promises to have a unique id.
        self.id = appid.gen()
        
        #Movement in the game world
        self._location = Vec2d(0., 0.)
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

    @property
    def location(self):
        """{int}  0 = lowest layer, no upper bound."""
        return self._location
    
    @location.setter
    def location(self, value):
        """  Set's layer value and sorts the viewports on this value.  """
        self._location = Vec2d(value)
        self.world.spatial_index.update(self)
        
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
                if self.speed < 0: self.speed = 1
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
        image = pygame.transform.rotate(self.image, self.direction*-1.)
        viewport.render_entity(image, x, y, self)  
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.speed > 0. and self.location != self.destination:
            self.move(time_passed) 

