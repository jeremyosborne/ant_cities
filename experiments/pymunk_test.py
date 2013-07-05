'''
Created on Jul 4, 2013

@author: john
'''

import pygame, math
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d

class Ant(object):
    
    def __init__(self):
        
        self.location = Vec2d(0.0, 0.0)
        self.velocity = Vec2d(0.0, 0.0)
        self.acceleration = Vec2d(0.0 ,0.0)
        self.max_steering_force = 0.0
        self.max_speed = 0.0
        self.graphic = pygame.image.load('../assets/red-ant.png')
        
    
#from gameobjects.vector2 import Vector2

start_position = Vec2d(20, 300)
end_position = Vec2d(20, 100)

destination = end_position
speed = 0.  #Our starting speed.
speed_up_acceleration = 10.
acceleration = speed_up_acceleration
target_speed = 20.
direction = 0.
slow_down_distance = 120.
slow_down_acceleration = -30.

current_heading = (destination - location)
current_heading = current_heading.normalized()

desired_heading = current_heading

steering_force = 360. #Degrees per second

#Steering force = desired velocity - current velocity

if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ant = Ant()

    ant.location = start_position
    ant.max_speed = 4
    ant.max_steering_force = 0.1
    
    clock = pygame.time.Clock()
    
    background = pygame.surface.Surface((800, 600)).convert()
    background.fill((0, 0, 0))

    #Show initial position
    screen.blit(background, (0,0))
    screen.blit(ant, (location))
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
                    destination = Vec2d(mouse_x, mouse_y)
                    acceleration = speed_up_acceleration
                
        time_passed = float(clock.tick(30)/1000.)
        
        if location != destination:
            #Acceleration code
            if acceleration > 0:  #Then we're accelerating.
                if speed < target_speed:
                    speed += acceleration * time_passed
            elif acceleration < 0:  #Then we're slowing down.
                if (speed + acceleration) > 0: 
                    speed += acceleration * time_passed
                else:
                    speed = (slow_down_acceleration / 2.) * -1.
                    
            vec_to_destination = destination - location       
            distance_to_destination = vec_to_destination.get_length()
            new_heading = vec_to_destination.normalized()
            print "New Heading: ", new_heading
            
            travel_distance = min(distance_to_destination, time_passed * speed)
            
            #Change current_heading towards the new heading
            #if current_heading != new_heading:
                
                #current_heading += steering_force                
            print "Current_heading: ", current_heading
              
            location += travel_distance * current_heading
            print "Travel Distance: ", travel_distance, "Distance_to_destination: ", distance_to_destination
            print "Speed: ", speed
            #Direction used for rotating the image.
            direction = (math.atan2(current_heading.y, current_heading.x)*(180/math.pi))
            print "Direction: ", direction, "heading.y: ", current_heading.y, "heading.x:", current_heading.x
            #Are we there yet?
            if distance_to_destination <= slow_down_distance:
                #replace with formula that takes into consideration current speed.
                #also change test, such that the slow down distance is also based
                #on the current speed.
                acceleration = slow_down_acceleration
                    
        screen.blit(background, (0,0))
        #screen.blit(ant, (location))
        screen.blit((pygame.transform.rotate(ant, (direction*-1.))), location)
        
        #Finalize
        pygame.display.update()