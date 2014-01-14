'''
Main run loop.

Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *
import globaldata

from gamesimulation import GameSimulation



def run():
    """Call to start the game.
    """
    
    pygame.init()
    pygame.display.set_caption(globaldata.GAME_TITLE)
    
    # Needs to be initialized after everything.
    game_simulation = GameSimulation()
    
    print pygame.display.Info()

    #Main game loop    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            else:
                game_simulation.ui_controller.handle_event(event)

        game_simulation.process()


