'''
Created on Jul 5, 2013

@author: john
'''

import pygame, math
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d

'''
Created on Jul 3, 2013

@author: john
'''

class Ant(object):

    def __init__ (self):
        
        self.location = Vec2d(600, 300) # Our default starting location.
        self.destination = Vec2d(20, 300) # Our default end position.
        self.current_heading = Vec2d(0, 0) # Where we're currently pointing.
        self.desired_heading = Vec2d(0, 0) # Where we want to be going.
        self.speed = 10.0 # Our starting speed.
        self.acceleration = 0.0 # Our current acceleration, can be + or -
        self.speed_up_acceleration = 10.
        self.slow_down_acceleration = -30.
        self.slow_down_distance = 120.  #Change this with a function
        self.max_speed = 120.
        self.direction = 0.  #Direction we're pointed to in degrees
        
        self.image = pygame.image.load('../assets/red-ant.png')

    def rotate_heading(self, vector, angle):
        
        new_x = vector.x * math.cos(angle) - vector.y * sin(angle)
        new_y = vector.y * math.sin(angle) + vector.y * cos(angle)
        return Vec2d(new_x, new_y)
    
    def degrees_to_rotate(self):
        pass

    def direction_to_rotate(self, current_heading_in_degrees, desired_heading_in_degrees):
        
        if current_heading_in_degrees < 0:
            current_heading_in_degrees = (current_heading_in_degrees * (-1.)) + 180
        if desired_heading_in_degrees < 0:
            desired_heading_in_degrees = (desired_heading_in_degrees * (-1.)) + 180
        
            
            
    def move(self):
        #Acceleration/speed code
        if ant.acceleration > 0:  #Then we're accelerating.
            if ant.speed < ant.max_speed:
                ant.speed += ant.acceleration * time_passed
        elif ant.acceleration < 0:  #Then we're slowing down.
            if (ant.speed + ant.acceleration) > 0: 
                ant.speed += ant.acceleration * time_passed
            else:
                ant.speed = (ant.slow_down_acceleration / 2.) * -1.
                
        vec_to_destination = ant.destination - ant.location
        distance_to_destination = vec_to_destination.get_length()
        self.desired_heading = vec_to_destination.normalized()
        #Determine if we should be steering in another direction.
        if self.current_heading != self.desired_heading:
            #Determine which way to steer.
            print "Desired Heading: ", self.desired_heading
            print "Heading: ", self.current_heading
            angle = self.current_heading.get_angle_degrees_between(self.desired_heading)
            print "Angle Between: ", angle
            #     
            #Steer current heading towards desired heading.
            #should we steer left or steer right.
            
            #Add or subtract to the current heading.
            
            #self.current_heading = self.desired_heading
            
            #current_heading_in_degrees = (math.atan2(self.heading.y, self.heading.x)*(180/math.pi))
            #print "Current heading in degrees: ", current_heading_in_degrees, self.heading.get_angle_degrees()
            #desired_heading_in_degrees = (math.atan2(self.desired_heading.y, self.desired_heading.x)*(180/math.pi))
            #print "Desired heading in degrees: ", desired_heading_in_degrees, self.desired_heading.get_angle_degrees()
            
        #Remove this line soon.
        #self.heading = self.desired_heading
        travel_distance = min(distance_to_destination, time_passed * ant.speed)
        ant.location += travel_distance * self.current_heading
        print "Travel Distance: ", travel_distance, "Distance_to_destination: ", distance_to_destination
        print "Speed: ", ant.speed, " location: ", ant.location
        
        #Direction used for rotating the image.
        self.direction = (math.atan2(self.current_heading.y, self.current_heading.x)*(180/math.pi))+90

        #Are we there yet?
        if distance_to_destination <= ant.slow_down_distance:
            #replace with formula that takes into consideration current speed.
            #also change test, such that the slow down distance is also based
            #on the current speed.
            ant.acceleration = ant.slow_down_acceleration




#acceleration = speed_up_acceleration



#current_heading = Vec2d(0., 1.)



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
        
    #Initial calcultions
    ant.destination = Vec2d(50, 150)
    
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
            ant.move()
                    
        screen.blit(background, (0,0))
        #screen.blit(ant, (location))
        screen.blit((pygame.transform.rotate(ant.image, (ant.direction*-1.))), ant.location)
        
        #Finalize
        pygame.display.update()