'''
Created on Jul 3, 2013

@author: john
'''

import pygame, math
from pygame.locals import *

from gameobjects.vector2 import Vector2

start_position = Vector2(20, 300)
end_position = Vector2(200, 100)

location = start_position
destination = end_position
speed = 0.  #Our starting speed.
acceleration = 10.
target_speed = 120.
direction = 0.


if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ant = pygame.image.load('../assets/red-ant.png')
    #ant = pygame.transform.rotate(ant, -90.)
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
                
        time_passed = float(clock.tick(30)/1000.)
        
        #Render and simulation spot.
        
        if speed < target_speed:
            speed += acceleration * time_passed
        vec_to_destination = destination - location
        print "vec_to_destination: ", vec_to_destination, " destination: ", destination, " location: ", location, "speed: ", speed       
        distance_to_destination = vec_to_destination.get_length()
        heading = vec_to_destination.get_normalized()
        print "heading: ", heading, " vector to destination: ", vec_to_destination
        travel_distance = min(distance_to_destination, time_passed * speed)
        location += travel_distance * heading
        
        direction = (math.atan2(heading.y, heading.x)*(180/math.pi))+90
        print "degree_heading: ", direction
        
        screen.blit(background, (0,0))
        #screen.blit(ant, (location))
        screen.blit((pygame.transform.rotate(ant, (direction*-1.))), location)
        
        #Finalize
        pygame.display.update()