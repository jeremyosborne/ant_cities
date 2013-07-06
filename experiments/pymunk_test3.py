'''
Created on Jul 6, 2013

@author: john
'''

import pygame, math
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d

class Ant(object):
    
    def __init__(self):
        
        self.location = Vec2d(600, 300) # Our default starting location.
        self.destination = Vec2d(600, 100) # Our default end position.
        self.current_heading = (self.destination - self.location).normalized()
        self.desired_heading = self.current_heading
        self.speed = 0 # Our starting speed.
        self.acceleration = 0.0 # Our current acceleration, can be + or -
        self.speed_up_acceleration = 30.
        self.slow_down_acceleration = -50.
        self.slow_down_distance = 120.  #Change this with a function
        self.max_speed = 120.
        self.direction = 0.  #Direction we're pointed to in degrees
        self.rotation_per_second = 90. # Degrees per second we can turn.
        
        self.image = pygame.image.load('../assets/red-ant.png')
    
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
        vec_to_destination = ant.destination - ant.location
        distance_to_destination = vec_to_destination.get_length()
        travel_distance = min(distance_to_destination, time_passed * ant.speed)
        self.location += travel_distance * self.current_heading
        
        #Apply acceleration forces.
        self.apply_acceleration(time_passed, distance_to_destination)
        self.direction = (math.atan2(self.current_heading.y, self.current_heading.x)*(180/math.pi))+90

        print "speed: ", self.speed
if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    ant = Ant()
    
    
    background = pygame.surface.Surface((800, 600)).convert()
    background.fill((0, 0, 0))

    #Show initial position
    screen.blit(background, (0,0))
    screen.blit(ant.image, (ant.location))
    pygame.display.update()
    time_passed = clock.tick(30)
    
    #run loop
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left click and new destination selected
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    ant.destination = Vec2d(mouse_x, mouse_y)
                    ant.acceleration = ant.speed_up_acceleration
                
        time_passed = float(clock.tick(30)/1000.)
        
        if ant.location != ant.destination:
            ant.move(time_passed)
                    
        screen.blit(background, (0,0))
        w, h = ant.image.get_size()
        screen.blit((pygame.transform.rotate(ant.image, (ant.direction*-1.))), (ant.location.x-w/2, ant.location.y-h/2))
        
        #Finalize
        pygame.display.update()
