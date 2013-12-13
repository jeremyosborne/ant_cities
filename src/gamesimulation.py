import pygame
from pygame.locals import *

import globaldata
import viewport
import time
from game import events
from world import World
from ui.minimap import MiniMap
from ui.viewunitinfobox import ViewUnitInfoBox
from ui.fpsdisplay import FPSDisplay
from ui.datacolumndisplay import DataColumnDisplay


class GameSimulation():
       
    def __init__(self):
                            
        #Normal pygame window mode.
        self.screen = pygame.display.set_mode(globaldata.screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        #Normal pygame full screen mode.
        #screen = pygame.display.set_mode(globaldata.screen_size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        #Set up game world
        
        #The minus 170 below is the y size of the UI elements.  
        self.world = World(globaldata.world_size_x, globaldata.world_size_y, globaldata.screen_size_x, globaldata.screen_size_y-170)
        
        #Setup UI elements.
        self.mini_map = MiniMap(globaldata.screen_size_x-256, globaldata.screen_size_y-170, 
                                256, 170, 
                                globaldata.world_size_x, globaldata.world_size_y, 
                                events)

        #Unit information display.
        self.unit_information_display = ViewUnitInfoBox(globaldata.screen_size_x-512, globaldata.screen_size_y-170, 
                                                        256, 170,
                                                        events)
          
        # FPS Display
        self.fps_display = FPSDisplay(5, 5)
        
        # Base Information Displays
        self.base_display_1 = DataColumnDisplay(1, globaldata.screen_size_y-170, 
                                                200, 170,
                                                "Base "+self.world.base_1.description,
                                                [
                                                 ("# Ants Born:", lambda: str(self.world.base_1.ant_born)),
                                                 ("# Ants Died:", lambda: str(self.world.base_1.ant_dead)),
                                                 ("# Ants Net:", lambda: str(self.world.base_1.ant_count)),
                                                 ("Energy:", lambda: str(self.world.base_1.energy_units)),
                                                 ("Leaf Storage:", lambda: str(self.world.base_1.leaves_returned)),
                                                ])
        self.base_display_2 = DataColumnDisplay(201, globaldata.screen_size_y-170, 
                                                200, 170,
                                                "Base "+self.world.base_2.description,
                                                [
                                                 ("# Ants Born:", lambda: str(self.world.base_2.ant_born)),
                                                 ("# Ants Died:", lambda: str(self.world.base_2.ant_dead)),
                                                 ("# Ants Net:", lambda: str(self.world.base_2.ant_count)),
                                                 ("Energy:", lambda: str(self.world.base_2.energy_units)),
                                                 ("Leaf Storage:", lambda: str(self.world.base_2.leaves_returned)),
                                                ])
        # World Info Display
        self.world_info_display = DataColumnDisplay(402, globaldata.screen_size_y-170, 
                                              200, 170,
                                              "World Info",
                                              [
                                                ("Leaves Born:", lambda: str(self.world.leaf_born)),
                                                ("Leaves Expired:", lambda: str(self.world.leaf_expired)),
                                                ("Leaves In World:", lambda: str(self.world.leaf_world_count)),
                                                ("Game Time:", lambda: str(int(time.time() - self.world.time_born))),
                                                ("Base Count:", lambda: str(self.world.base_count)),
                                              ])
        
        self.clock = pygame.time.Clock()

    def process_game_loop(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)

        self.world.process(time_passed)

        self.world.viewport.update()
        self.mini_map.update(self.world, draw=globaldata.render_minimap)
        self.fps_display.update(self.clock)
        self.unit_information_display.update(self.world)  
        self.base_display_1.update()
        self.base_display_2.update()
        self.world_info_display.update() 

        self.world.render(draw=globaldata.render_world)

        # Call the method that renders all the viewport layers in the proper sequence.
        viewport.Viewport.render_viewports(self.screen)
        
        pygame.display.flip()
