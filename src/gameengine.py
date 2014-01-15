import pygame
from pygame.locals import *

import globaldata
from world import World
from ui.minimap import MiniMap
from ui.unitinfobox import UnitInfoBox
from ui.fpsdisplay import FPSDisplay
from ui.datacolumndisplay import DataColumnDisplay
from ui.map import Map
from ui.mousedisplay import MouseDisplay
from ui.controllers import GameUIController
from ui.assets.imageassets import ImageAssets
from ui.pygameview import PygameDisplay


class GameEngine():
    """The main game object, responsible for running the simulation and the
    ui.
    """
    def __init__(self):
        """Initialize game simulation.
        
        imageassets {AssetCache} Image cache.
        """
        
        # Reference to the globaldata for our application.
        self.globaldata = globaldata
        
        # Reference to the game clock for handling framerate.
        self.clock = pygame.time.Clock()
        
        self.world = World(globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1])

        # -------------------------------------------- UI
        
        # Cache of image assets.
        self.imageassets = ImageAssets(globaldata.ASSETS_PATH)

        # Controller for all UI elements.
        self.ui_controller = GameUIController(self)

        # The main display, which all other views should be nested with.
        # Display needs to be set before any graphics calls.
        self.display = PygameDisplay(0, 0, globaldata.SCREEN_SIZE[0], globaldata.SCREEN_SIZE[1], 0, self.ui_controller)

        # The minus 170 below is the y size of the UI elements.
        self.display.addchild(Map(self.display.x, self.display.y, 
                                 self.display.width, self.display.height-170, 0,
                                 self.ui_controller))
        
        # Frames per second.
        self.display.addchild(FPSDisplay(5, 5, 250, 20, 0, self.ui_controller))
        
        # Mouse coordinates.
        self.display.addchild(MouseDisplay(5, 25, 250, 20, 0, self.ui_controller))
        
        # Mini map.
        self.display.addchild(MiniMap(self.display.width-256, self.display.height-170, 
                                256, 170, 0,
                                self.ui_controller))

        # Unit information display.
        self.display.addchild(UnitInfoBox(self.display.width-512, self.display.height-170, 
                                 256, 170, 0,
                                 self.ui_controller))
        
        # Player Base Information
        data_to_display = [
            ("Ants:", lambda: str(len(filter(lambda e: hasattr(e, "base") and e.base == self.world.anthill_1, self.world.entities.itervalues())))),
            ("Energy:", lambda: str(self.world.anthill_1.c["energy"].val)),
        ]
        self.display.addchild(DataColumnDisplay(self.display.x, self.display.height-170, 
                                                200, 170,
                                                title=str(self.world.anthill_1.c["team"]),
                                                data=data_to_display))

        # World Info Display
        data_to_display = [
            ("Game Time:", lambda: str(int(self.world.age))),
            ("Leaves:", lambda: str(len(filter(lambda e: e.name == "leaf", self.world.entities.itervalues())))),
        ]
        self.display.addchild(DataColumnDisplay(self.display.x+402, self.display.height-170, 
                                              200, 170,
                                              title="World Info",
                                              data=data_to_display))

    def process(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)
        
        # Update logic.
        self.world.process(time_passed)

        # Update UI.
        self.display.render()
