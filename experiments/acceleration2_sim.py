'''
Created on Jul 3, 2013

@author: john
'''

import pygame, math
from pygame.locals import *

from gameobjects.vector2 import Vector2

start_position = Vector2(20, 300)
end_position = Vector2(20, 100)

location = start_position
destination = end_position
speed = 0.  #Our starting speed.
speed_up_acceleration = 10.
acceleration = speed_up_acceleration
target_speed = 120.
direction = 0.
slow_down_distance = 120.
slow_down_acceleration = -30.
current_heading = Vector2(0., 1.)



if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ant = pygame.image.load('../assets/red-ant.png')
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
                    destination = Vector2(mouse_x, mouse_y)
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
            heading = vec_to_destination.get_normalized()
            print "Heading: ", heading
            travel_distance = min(distance_to_destination, time_passed * speed)
            location += travel_distance * heading
            print "Travel Distance: ", travel_distance, "Distance_to_destination: ", distance_to_destination
            print "Speed: ", speed
            #Direction used for rotating the image.
            direction = (math.atan2(heading.y, heading.x)*(180/math.pi))+90
    
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