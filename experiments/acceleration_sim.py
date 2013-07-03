'''
Created on Jul 2, 2013

@author: john
'''

import pygame, math, sys
from pygame.locals import *

from gameobjects.vector2 import Vector2

start_position = Vector2(20, 300)
end_position = Vector2(780, 300)

location = start_position
velocity = Vector2(0,0)
acceleration = Vector2(0.05, 0.0)
topspeed = 5


if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ant = pygame.image.load('../assets/ant.png')
    clock = pygame.time.Clock()
    
    background = pygame.surface.Surface((800, 600)).convert()
    background.fill((0, 0, 0))

    #Show initial position
    screen.blit(background, (0,0))
    screen.blit(ant, (location))
    pygame.display.update()
        
    #run loop
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                
        time_passed = clock.tick(30)
        
        #Render and simulation spot.
        if velocity.get_x() < topspeed:
            velocity += acceleration
        location += velocity
        

        
        screen.blit(background, (0,0))
        screen.blit(ant, (location))
        
        #Finalize
        pygame.display.update()
        