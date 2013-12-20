import pygame
from pygame.locals import *

import globaldata
import viewport
import time
from world import World
from ui.minimap import MiniMap
from ui.viewunitinfobox import ViewUnitInfoBox
from ui.fpsdisplay import FPSDisplay
from ui.datacolumndisplay import DataColumnDisplay
from ui.worldviewport import WorldViewport
from ui.mousedisplay import MouseDisplay

class GameSimulation():
       
    def __init__(self, events, imageassets):
        """Initialize game simulation.
        
        events {EventPublisher} Central event publisher.
        imageassets {AssetCache} Image cache.
        """

        self.clock = pygame.time.Clock()

        # Display needs to be set before any graphics calls.
        #Normal pygame window mode.
        self.screen = pygame.display.set_mode(globaldata.SCREEN_SIZE, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        #Normal pygame full screen mode.
        #screen = pygame.display.set_mode(globaldata.SCREEN_SIZE, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        #Set up game world

        #The minus 170 below is the y size of the UI elements.  
        self.world = World(globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1],
                           imageassets)

        # viewport is the screen entity that contains the view of the game world.
        self.world_viewport = WorldViewport(globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1], 
                                      globaldata.SCREEN_SIZE[0], globaldata.SCREEN_SIZE[1]-170,
                                      events, imageassets)
        
        #Setup UI elements.
        self.mini_map = MiniMap(globaldata.SCREEN_SIZE[0]-256, globaldata.SCREEN_SIZE[1]-170, 
                                256, 170, 
                                globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1], 
                                events)

        #Unit information display.
        self.unit_information_display = ViewUnitInfoBox(globaldata.SCREEN_SIZE[0]-512, globaldata.SCREEN_SIZE[1]-170, 
                                                        256, 170,
                                                        events, imageassets)
          
        # FPS Display
        self.fps_display = FPSDisplay(5, 5)
        
        self.mouse_display = MouseDisplay(5, 25)
        
        # Base Information Displays
        self.base_display_1 = DataColumnDisplay(1, globaldata.SCREEN_SIZE[1]-170, 
                                                200, 170,
                                                str(self.world.base_1),
                                                [
                                                 ("# Ants Born:", lambda: str(self.world.base_1.ant_born)),
                                                 ("# Ants Died:", lambda: str(self.world.base_1.ant_dead)),
                                                 ("# Ants Net:", lambda: str(self.world.base_1.ant_count)),
                                                 ("Energy:", lambda: str(self.world.base_1.energy_units)),
                                                 ("Leaf Storage:", lambda: str(self.world.base_1.leaves_returned)),
                                                ])
        self.base_display_2 = DataColumnDisplay(201, globaldata.SCREEN_SIZE[1]-170, 
                                                200, 170,
                                                str(self.world.base_2),
                                                [
                                                 ("# Ants Born:", lambda: str(self.world.base_2.ant_born)),
                                                 ("# Ants Died:", lambda: str(self.world.base_2.ant_dead)),
                                                 ("# Ants Net:", lambda: str(self.world.base_2.ant_count)),
                                                 ("Energy:", lambda: str(self.world.base_2.energy_units)),
                                                 ("Leaf Storage:", lambda: str(self.world.base_2.leaves_returned)),
                                                ])
        # World Info Display
        self.world_info_display = DataColumnDisplay(402, globaldata.SCREEN_SIZE[1]-170, 
                                              200, 170,
                                              "World Info",
                                              [
                                                ("Game Time:", lambda: str(int(time.time() - self.world.time_born))),
                                                ("Bases:", lambda: str(self.world.stats["base"])),
                                                ("Leaves:", lambda: str(self.world.stats["leaf"])),
                                                ("Leaves Added:", lambda: str(self.world.stats["leaves-added"])),
                                                ("Leaves Removed:", lambda: str(self.world.stats["leaves-removed"])),
                                              ])

    def process_game_loop(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)

        self.world.process(time_passed)

        self.world_viewport.update(self.world, draw=globaldata.render_world)
        self.mini_map.update(self.world, self.world_viewport, draw=globaldata.render_minimap)
        self.unit_information_display.update(self.world_viewport)  
        self.base_display_1.update()
        self.base_display_2.update()
        self.world_info_display.update()
        # Dev/debug.
        self.fps_display.update(self.clock)
        self.mouse_display.update(self.world_viewport)

        # Call the method that renders all the viewport layers in the proper sequence.
        viewport.Viewport.render_viewports(self.screen)
        
        pygame.display.flip()
