'''
Created on Mar 2, 2013

@author: jmadams
'''

import pygame
from pygame.locals import *

from random import randint, choice
import pymunk
from pymunk.vec2d import Vec2d

import game_world
import entities
import statemachines
import global_data
import viewport
import ui_elements

class Game_Simulation():
       
    def __init__(self):
                            
        #Normal pygame window mode.
        self.screen = pygame.display.set_mode(global_data.screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
      
        #Normal pygame full screen mode.
        #screen = pygame.display.set_mode(global_data.screen_size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        #Set up game world
        
        print pygame.display.Info()
          
        self.world = game_world.World(global_data.world_size_x, global_data.world_size_y, global_data.screen_size_x, global_data.screen_size_y)
        
        #Setup UI elements.
        #Mini_Map Init
        self.mini_map = ui_elements.Mini_Map(global_data.screen_size_x-256, global_data.screen_size_y-170, 256, 170, global_data.world_size_x, global_data.world_size_y)

        #Unit information display.
        self.unit_information_display = ui_elements.View_Unit_Info_Box(global_data.screen_size_x-512, global_data.screen_size_y-170, 256, 170)
          
        #FPS Display
        self.fps_display = ui_elements.FPS_Display()
        self.clock = pygame.time.Clock()
        
        self.render_game_world = True
    
        self.display_minimap = True
    

    def process_game_loop(self):
    
        #Let's take care of the mouse pointer location in terms of scrolling the map at screen border.            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 10:
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x - self.world.viewport.scroll_speed, self.world.viewport.world_viewable_center_y)    
        if mouse_x > (self.world.viewport.width-10):
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x + self.world.viewport.scroll_speed, self.world.viewport.world_viewable_center_y)    
        if mouse_y < 10:
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x, self.world.viewport.world_viewable_center_y - self.world.viewport.scroll_speed)    
        if mouse_y > (self.world.viewport.height-10):
            self.world.viewport.update_viewport_center(self.world.viewport.world_viewable_center_x, self.world.viewport.world_viewable_center_y + self.world.viewport.scroll_speed)
            
        #Time_passed is in miliseconds.
        time_passed = self.clock.tick(30)

        self.world.process(time_passed)
        if self.render_game_world:
            self.world.render()
        
        #Let's process the Mini_Map
        if self.display_minimap == True:
            self.mini_map.update(self.world)
        
        self.fps_display.draw_fps(self.clock)
                
        #Call the method that renders all the viewport layers in the proper sequence.
        viewport.Viewport.render_viewports(self.screen)
        
        #pygame.display.update()
        pygame.display.flip()
        
        
def run():
    
    pygame.init()

    game_simulation = Game_Simulation()
        
    #Main game loop    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_TAB:
                    if pygame.event.get_grab():
                        pygame.event.set_grab(False)
                    else:
                        pygame.event.set_grab(True)
                if event.key == K_q:
                    if game_simulation.render_game_world:
                        game_simulation.render_game_world = False
                    else:
                        game_simulation.render_game_world = True
                if event.key == K_m:  #Turn mini-map on
                    game_simulation.display_minimap = True
                if event.key == K_n:  #Turn mini-map off
                    game_simulation.display_minimap = False
                if event.key == K_c:  #Crash the program
                    game_simulation.mini_map.delete_me()
                    del game_simulation.mini_map
                if event.key == K_r:  #resize the game window.
                    game_simulation.world.viewport.height = 500
            #Handle the mouse wheel for zooming.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  #Mouse Scroll Wheel Up, so zoom in
                    game_simulation.world.viewport.change_zoom_level("in")
                elif event.button == 5:  #Mouse Scroll Wheel Down, so zoom out
                    game_simulation.world.viewport.change_zoom_level("out")
                else:
                    #Let's send it over to the viewport class to determine which
                    #viewport should process the input.
                    viewport.Viewport.route_event(event, game_simulation)
            if event.type == pygame.MOUSEBUTTONUP:
                #print "Mouse button up event."
                pass
            
        game_simulation.process_game_loop()
            
if __name__ == "__main__":    
    run()
    exit()
    

