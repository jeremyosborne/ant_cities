'''
Main run loop.

Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *
import globaldata

from events import EventPublisher
# Do before loading GameSimulation.
events = EventPublisher()

from ui.imageassets import ImageAssets
# Do before loading GameSimulation.
imageassets = ImageAssets(globaldata.ASSETS_PATH)

from gamesimulation import GameSimulation

def run():
    """Call to start the game.
    """
    global events
    
    pygame.init()
    pygame.display.set_caption(globaldata.GAME_TITLE)

    game_simulation = GameSimulation()

    print pygame.display.Info()

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
                    globaldata.render_world = not globaldata.render_world
                if event.key == K_m: 
                    # Toggle rendering of the mini-map.
                    globaldata.render_minimap = not globaldata.render_minimap
                if event.key == K_r:  
                    # Resize the game window.
                    game_simulation.world.viewport.height = 500
            elif event.type == MOUSEBUTTONDOWN:
                events.pub("MOUSEBUTTONDOWN", ev=event, game_sim=game_simulation)
            elif event.type == MOUSEBUTTONUP:
                events.pub("MOUSEBUTTONUP", ev=event, game_sim=game_simulation)
            elif event.type == MOUSEMOTION:
                events.pub("MOUSEMOTION", ev=event, game_sim=game_simulation)

        game_simulation.process_game_loop()


