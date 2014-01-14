import pygame
from pygame.locals import *

import globaldata
import ui.viewport as viewport
import time
from world import World
from ui.minimap import MiniMap
from ui.unitinfobox import UnitInfoBox
from ui.fpsdisplay import FPSDisplay
from ui.datacolumndisplay import DataColumnDisplay
from ui.worldviewport import WorldViewport
from ui.mousedisplay import MouseDisplay
from ui.controllers import GameUIController

class GameSimulation():
       
    def __init__(self, imageassets):
        """Initialize game simulation.
        
        imageassets {AssetCache} Image cache.
        """
        
        # Reference to the globaldata for our application.
        self.globaldata = globaldata
        
        # Reference to the game clock for handling framerate.
        self.clock = pygame.time.Clock()
        
        self.world = World(globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1])

        # -------------------------------------------- UI

        # Display needs to be set before any graphics calls.
        # Window mode.
        self.screen = pygame.display.set_mode(globaldata.SCREEN_SIZE, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        # Full screen mode.
        #screen = pygame.display.set_mode(globaldata.SCREEN_SIZE, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

        # Do we have a unit selected?
        self.ui_controller = GameUIController(self)

        # The current stack of ui elements.
        self.ui_views = []

        # viewport is the screen entity that contains the view of the game world.
        # The minus 170 below is the y size of the UI elements.
        self.world_viewport = WorldViewport(globaldata.SCREEN_SIZE[0], globaldata.SCREEN_SIZE[1]-170,
                                            self.ui_controller)
        self.ui_views.append(self.world_viewport)
        
        # Frames per second.
        self.ui_views.append(FPSDisplay(5, 5, self.ui_controller))
        
        # Mouse coordinates.
        self.ui_views.append(MouseDisplay(5, 25, self.ui_controller))
        
        # Mini map.
        self.ui_views.append(MiniMap(globaldata.SCREEN_SIZE[0]-256, globaldata.SCREEN_SIZE[1]-170, 
                                256, 170, 
                                self.ui_controller))

        # Unit information display.
        self.ui_views.append(UnitInfoBox(globaldata.SCREEN_SIZE[0]-512, globaldata.SCREEN_SIZE[1]-170, 
                                 256, 170,
                                 self.ui_controller, imageassets))
        
        # Base 1 Display
        data_to_display = [
            ("Ants:", lambda: str(len(filter(lambda e: hasattr(e, "base") and e.base == self.world.base_1, self.world.entities.itervalues())))),
            ("Energy:", lambda: str(self.world.base_1.c["energy"].val)),
        ]
        self.ui_views.append(DataColumnDisplay(1, globaldata.SCREEN_SIZE[1]-170, 
                                        200, 170,
                                        str(self.world.base_1.c["team"]),
                                        data_to_display))

        # Base 2 Display        
        data_to_display = [
            ("Ants:", lambda: str(len(filter(lambda e: hasattr(e, "base") and e.base == self.world.base_2, self.world.entities.itervalues())))),
            ("Energy:", lambda: str(self.world.base_2.c["energy"].val)),
        ]        
        self.ui_views.append(DataColumnDisplay(201, globaldata.SCREEN_SIZE[1]-170, 
                                        200, 170,
                                        str(self.world.base_2.c["team"]),
                                        data_to_display))

        # World Info Display
        data_to_display = [
            ("Game Time:", lambda: str(int(self.world.age))),
            ("Leaves:", lambda: str(len(filter(lambda e: e.name == "leaf", self.world.entities.itervalues())))),
        ]
        self.ui_views.append(DataColumnDisplay(402, globaldata.SCREEN_SIZE[1]-170, 
                                              200, 170,
                                              "World Info",
                                              data_to_display))

    def process(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)
        
        # Update logic.
        self.world.process(time_passed)

        # Update UI.
        for v in self.ui_views:
            v.update()
            v.render(self.screen)

        pygame.display.flip()
