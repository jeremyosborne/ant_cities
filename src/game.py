'''
Main run loop.

Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *

import viewport
import global_data
from gamesimulation import GameSimulation
from events import events

def run():
    """Call to start the game.
    """
    pygame.init()
    pygame.display.set_caption("Ant Cities")

    game_simulation = GameSimulation()
        
    #Main game loop    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Quit.
                    return
                if event.key == K_TAB:
                    # Grab the mouse
                    pygame.event.set_grab(not pygame.event.get_grab())
                if event.key == K_q: 
                    # Toggle rendering of the game world.
                    global_data.render_world = not global_data.render_world
                if event.key == K_m: 
                    # Toggle rendering of the mini-map.
                    global_data.render_minimap = not global_data.render_minimap
                if event.key == K_r:  
                    # Resize the game window.
                    game_simulation.world.viewport.height = 500
            elif event.type == MOUSEBUTTONDOWN:
                events.pub("MOUSEBUTTONDOWN", ev=event, game_sim=game_simulation)
                # Let's send it over to the viewport class to determine which
                # viewport should process the input.
                viewport.Viewport.route_event(event, game_simulation)
            elif event.type == MOUSEBUTTONUP:
                events.pub("MOUSEBUTTONUP", ev=event, game_sim=game_simulation)
                viewport.Viewport.route_event(event, game_simulation)
            elif event.type == MOUSEMOTION:
                events.pub("MOUSEMOTION", ev=event, game_sim=game_simulation)


        game_simulation.process_game_loop()


