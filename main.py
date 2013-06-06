"""
Run this file from the commandline to start.
"""

if __name__ == "__main__":
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

    
    # Import and initialize our modules.
#    import settings
#    from logger import log
    

    # The game module exports a game instance.
    # It is our job to call run on this game object to start the game. 
    import game
    game.run()
    print "Game has exited if we are here. All necessary cleanup should have happened before this point."
    print "Thank you for playing."





#To Do stuff:
#Levers for the simulation:
#Hostility level
#Friendly index
#Helpful level
#Health minded ants or self sacrafice?
#Expansionn oriented or homebodies?
#Conversion or kill?

#evolutionary advancements
#vision increase
#conversion capability

#Food is converted into:
#food for the ants
#new ants
#evolutionary advancements 

#Different Ant types
#New food types


#The Swarm
