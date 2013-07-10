'''
Created on Jul 9, 2013

@author: john

The purpose of this experiment is to determine performance
characteristics of blitting on various sized surfaces.

'''

import pygame, math
from pygame.locals import *
from random import randint

screen_size_x = 800
screen_size_y = 600
#For larger than screen size surface

scale_factor = 5
number_of_entities_to_blit = 200
image = pygame.image.load('../assets/red-ant.png')

def get_random_location():
    x = randint(0,screen_size_x)
    y = randint(0,screen_size_y)
    return (x, y)

def experiment_1(surface):
    """ Purpose:  render game elements only on the main surface. """
    
    for i in range(1, number_of_entities_to_blit):
        location = get_random_location()
        surface.blit(image, location)
        
def experiment_2(screen, surface, background):
    """ Purpose:  render game elements on the non screen surface, then onto
    the main surface."""

    surface.blit(background, (0,0))
    for i in range(1, number_of_entities_to_blit):
        location = get_random_location()
        surface.blit(image, location)
    screen.blit(surface, (0, 0))
    
def experiment_3(screen, surface, background):
    """ Purpose:  Render game elements on much larger surface.  For this test,
    we are not going to blit the larger surface scaled back to the screen surface.
    That way, we are only measuring the time needed to deal with a larger surface
    and not the time it takes to take the larger surface and scale back to screen
    size."""
    
    surface.blit(background, (0,0))
    for i in range(1, number_of_entities_to_blit):
        location = get_random_location()
        surface.blit(image, location)
    #screen.blit(surface, (0, 0))
    
    """ Purpose:  Render game elements on much larger surface """
    
def experiment_4():
    """  Purpose:  render game elements as squares on main surface."""
     
def experiment_5():
    """  Purpose:  render game elements as squares on secondary surface
    then copied to the main surface."""
    
if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((screen_size_x, screen_size_y))
    secondary_surface = pygame.surface.Surface((screen_size_x, screen_size_y)).convert()
    big_surface = pygame.surface.Surface((screen_size_x*scale_factor, screen_size_y*scale_factor)).convert()
    clock = pygame.time.Clock()
    background = pygame.surface.Surface((screen_size_x, screen_size_y)).convert()
    background.fill((0, 0, 0))
    big_background = pygame.surface.Surface((screen_size_x*scale_factor, screen_size_y*scale_factor)).convert()
    big_background.fill((0, 0, 0))
    
    font = pygame.font.SysFont("arial", 16);
    
    #run loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                
        time_passed = float(clock.tick(60)/1000.)
        
        #clear the screen
        screen.blit(background, (0,0))
    
    #--------------------------------------------------------------------------------------------------
    #Just uncomment the experiment you would like to run.
    #Descriptions of each experiment are above with the procedure.
    #--------------------------------------------------------------------------------------------------
        #experiment_1(screen)
        #experiment_2(screen, secondary_surface, background)
        experiment_3(screen, big_surface, big_background)
        
    #--------------------------------------------------------------------------------------------------    
        #Print FPS to screen
        fps = clock.get_fps()
        label = font.render(str(fps), True, (255, 255, 255))
        screen.blit(label, (0, 0))
            
        #Finalize
        pygame.display.update()