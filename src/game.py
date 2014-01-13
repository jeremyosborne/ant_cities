'''
Main run loop.

Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *
import globaldata

from ui.assets.imageassets import ImageAssets
from gamesimulation import GameSimulation



# Globals, to be initialized during run time.
imageassets = None
game_simulation = None



def run():
    """Call to start the game.
    """
    global game_simulation, imageassets
    
    pygame.init()
    pygame.display.set_caption(globaldata.GAME_TITLE)

    imageassets = ImageAssets(globaldata.ASSETS_PATH)
    
    # Needs to be initialized after everything.
    game_simulation = GameSimulation(imageassets)
    
    print pygame.display.Info()

    #Main game loop    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            else:
                game_simulation.ui_controller.handle_event(event)

        game_simulation.process()


