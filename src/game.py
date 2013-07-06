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
                
def run():
    
    pygame.init()
    screen = pygame.display.set_mode(global_data.screen_size, 0, 32)
  
    #Set up game world  
    world = game_world.World(global_data.world_size_x, global_data.world_size_y, global_data.screen_size_x, global_data.screen_size_y)
    
    #Setup UI elements.
    #Mini_Map Init
    mini_map = ui_elements.Mini_Map(1000-256, 700-170, 256, 170, global_data.world_size_x, global_data.world_size_y)
    mini_map.description = "Mini Map"

    #FPS Display
    fps_display = ui_elements.FPS_Display()
    clock = pygame.time.Clock()
    
    render_game_world = True

    #Main game loop    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_3:
                    world.viewport.update_zoom_level(world.viewport.zoom_level_3)
                if event.key == K_1:
                    world.viewport.update_zoom_level(world.viewport.zoom_level_1)
                if event.key == K_2:
                    world.viewport.update_zoom_level(world.viewport.zoom_level_2)
                if event.key == K_4:
                    world.viewport.update_zoom_level(world.viewport.zoom_level_4)
                if event.key == K_5:
                    world.viewport.update_zoom_level(world.viewport.zoom_level_5)
                if event.key == K_q:
                    if render_game_world:
                        render_game_world = False
                    else:
                        render_game_world = True
                if event.key == K_m:  #Turn mini-map on
                    mini_map.turn_on()
                if event.key == K_n:  #Turn mini-map off
                    mini_map.turn_off()
                if event.key == K_c:  #Crash the program
                    mini_map.delete_me()
                    del mini_map
                if event.key == K_r:  #resize the game window.
                    world.viewport.height = 500
            #Handle the mouse wheel for zooming.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  #Mouse Scroll Wheel Up, so zoom in
                    world.viewport.change_zoom_level("in")
                if event.button == 5:  #Mouse Scroll Wheel Down, so zoom out
                    world.viewport.change_zoom_level("out")
                
        #Let's take care of the mouse.            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 10:
            world.viewport.subtract_from_viewport_x(world.viewport.scroll_speed)
                
        if mouse_x > (world.viewport.width-10):
            world.viewport.add_to_viewport_x(world.viewport.scroll_speed)
                
        if mouse_y < 10:
            world.viewport.subtract_from_viewport_y(world.viewport.scroll_speed)
                
        if mouse_y > (world.viewport.height-10):
            world.viewport.add_to_viewport_y(world.viewport.scroll_speed)
        
        #Time_passed is in miliseconds.
        time_passed = clock.tick(60)

        world.process(time_passed)
        if render_game_world:
            world.render()
        
        #Let's process the Mini_Map
        mini_map.update(world)
        
        fps_display.draw_fps(clock)
                
        #Call the method that renders all the viewport layers in the proper sequence.
        viewport.Viewport.render_viewports(screen)
        
        pygame.display.update()
    
if __name__ == "__main__":    
    run()
    exit()
    

