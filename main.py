"""
Run this file from the commandline to start.
"""
import sys
import os

# This is a special case in our potentially complex program.
# Define the PYTHONPATH here because we want to make sure that all
# modules at all times, even here, stick to a particular naming
# convention.
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),"src")))
# From here on, to protect potential initialization code in .py files,
# treat the src/ directory as the root directory for imports and append
# folder names of subfolders/packages of src to the import names.
# This will prevent init scripts from running more than once.
# There is a discussion for why this is so here:
# http://python-notes.boredomandlaziness.org/en/latest/python_concepts/import_traps.html

import pygame
from gameengine import GameEngine



def run():
    """Call to start the game.
    """
    
    pygame.init()
    
    # Needs to be initialized after everything.
    game_engine = GameEngine()

    if __debug__:
        print pygame.display.Info()

    #Main game loop    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            else:
                game_engine.ui_controller.handle_event(event)

        game_engine.process()



if __name__ == "__main__":
    # The game module exports a game instance.
    # It is our job to call run on this game object to start the game. 
    run()
    print "Thank you for playing."
