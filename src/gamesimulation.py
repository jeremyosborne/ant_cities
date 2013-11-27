import pygame
from pygame.locals import *

import global_data
import viewport
from world import World
from ui.minimap import MiniMap
from ui.view_unit_info_box import View_Unit_Info_Box
from ui.fpsdisplay import FPSDisplay
from ui.base_panel import Base_Panel
from ui.world_panel import World_Panel


class GameSimulation():
       
    def __init__(self):
                            
        #Normal pygame window mode.
        self.screen = pygame.display.set_mode(global_data.screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        #Normal pygame full screen mode.
        #screen = pygame.display.set_mode(global_data.screen_size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        #Set up game world
        
        print pygame.display.Info()
        
        #The minus 170 below is the y size of the UI elements.  
        self.world = World(global_data.world_size_x, global_data.world_size_y, global_data.screen_size_x, global_data.screen_size_y-170)
        
        #Setup UI elements.
        self.mini_map = MiniMap(global_data.screen_size_x-256, global_data.screen_size_y-170, 256, 170, global_data.world_size_x, global_data.world_size_y)

        #Unit information display.
        self.unit_information_display = View_Unit_Info_Box(global_data.screen_size_x-512, global_data.screen_size_y-170, 256, 170)
          
        #FPS Display
        self.fps_display = FPSDisplay()
        
        #Base Display 1
        self.base_display_1 = Base_Panel(self.world.base_2, 1, global_data.screen_size_y-170, 200, 170)
        self.base_display_2 = Base_Panel(self.world.base_1, 201, global_data.screen_size_y-170, 200, 170)
        
        #World Info Display
        self.world_info_display = World_Panel(self.world, 402, global_data.screen_size_y-170, 200, 170)
        
        self.clock = pygame.time.Clock()

    def process_game_loop(self):
    
        #Let's take care of the mouse pointer location in terms of scrolling the map at screen border.
        #Since the game world's viewport dimensions are likely to be different than the screen size, we should change the dependent variables below, for example
        #rather than using world.viewport.height, use the screen height - that is, if you want the scrolling action to really take place at the edge of the screen
        #rather than the edge of the world viewport.  Made manual adjustment below with +170 until I've thought is through.            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 10:
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x - self.world.viewport.scroll_speed, self.world.viewport.world_viewable_center_y)    
        if mouse_x > (self.world.viewport.width-10):
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x + self.world.viewport.scroll_speed, self.world.viewport.world_viewable_center_y)    
        if mouse_y < 10:
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x, self.world.viewport.world_viewable_center_y - self.world.viewport.scroll_speed)    
        if mouse_y > (self.world.viewport.height-10+170):
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x, self.world.viewport.world_viewable_center_y + self.world.viewport.scroll_speed)
            
        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)

        self.world.process(time_passed)

        self.mini_map.update(self.world, draw=global_data.render_minimap)
        self.fps_display.update(self.clock)
        self.unit_information_display.update(self.world)  
        self.base_display_1.update()
        self.base_display_2.update()
        self.world_info_display.update() 

        self.world.render(draw=global_data.render_world)

        # Call the method that renders all the viewport layers in the proper sequence.
        viewport.Viewport.render_viewports(self.screen)
        
        pygame.display.flip()
