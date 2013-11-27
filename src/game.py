'''
Main run loop.

Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *

import viewport
from gamesimulation import GameSimulation

def run():
    """Call to start the game.
    """
    pygame.init()

    game_simulation = GameSimulation()
        
    #Main game loop    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Quit.
                    return
                if event.key == K_TAB:
                    # Grab the mouse
                    pygame.event.set_grab(not pygame.event.get_grab())
                if event.key == K_q: 
                    # Toggle rendering of the game world.
                    game_simulation.render_game_world = not game_simulation.render_game_world
                if event.key == K_m: 
                    # Toggle rendering of the mini-map.
                    game_simulation.display_minimap = not game_simulation.display_minimap
                if event.key == K_r:  
                    # Resize the game window.
                    game_simulation.world.viewport.height = 500
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Let's send it over to the viewport class to determine which
                # viewport should process the input.
                viewport.Viewport.route_event(event, game_simulation)
            
        game_simulation.process_game_loop()


