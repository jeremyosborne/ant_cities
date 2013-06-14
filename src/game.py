'''
Created on Mar 2, 2013

@author: jmadams
'''

#screen_size = (1200, 768)
#WORLD_SIZE = (1200, 512)
#INTERFACE_SIZE = (1200, 256)
#NEST_POSITION = (944, 256)
#NEST_POSITION_2 = (256, 256)
#ANT_COUNT = 20
#NEST_SIZE = 5.

import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

import entities
import statemachines
import global_data
import viewport
import ui_elements
       

class World(object):
    
    def __init__(self, x, y):
        
        #The size of the world for x and y
        self.width = x
        self.height = y
        
        self.entities = {}    #Dictionary of all the entities
        self.entity_id = 0
        #viewport is the screen entity that contains the view of the game world.
        self.viewport = ui_elements.World_Viewport(self.width, self.height)
        self.sri = False

        
    def add_entity(self, entity):   #The entity is whatever game entity object is being passed in.
        
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    def remove_entity(self, entity):
        
        del self.entities[entity.id]
                
    def get(self, entity_id):
        
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
        
    def process(self, time_passed):
                
        time_passed_seconds = time_passed / 1000.0        
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            
    def render(self, surface):
        
        #Prepares for the next frame.  Clears the background, etc.
        self.viewport.prepare_new_frame()
        
        #Render each entity onto the framebuffer.
        for entity in self.entities.itervalues():
            entity.render(self.viewport)
        #Render the framebuffer onto the screen    
        self.viewport.render(surface)
        
            
    def get_close_entity(self, name, location, range=100.):
        
        location = Vector2(*location)        
        
        for entity in self.entities.itervalues():            
            if entity.name == name:                
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity        
        return None

    def count(self, name):
        entity_count = 0
        for entity in self.entities.itervalues():
            if entity.name == name:
                entity_count += 1
        return entity_count
    
    def add_sri(self):
        self.sri = True
                
def print_fps(clock, screen):
    
    fps = clock.get_fps()
    
    #Since we're stopping normal rendering, we have clear the area where the text will be written.
    pygame.draw.rect(screen, (255, 255, 255), (5, global_data.screen_size_y - 50, 125, 20), 0)
    font = pygame.font.SysFont("arial", 16);
    label = font.render(str(fps), True, (0, 0, 0))
    screen.blit(label, (5, global_data.screen_size_y - 50))
    
def run():
    
    pygame.init()
    screen = pygame.display.set_mode(global_data.screen_size, 0, 32)
    
    world = World(global_data.world_size_x, global_data.world_size_y)
    #control_panel = ControlPanel(world)
    
    #Mini_Map Init
    mini_map = ui_elements.Mini_Map(1000-256, 700-170, 256, 170, global_data.world_size_x, global_data.world_size_y)
    #mini_map.turn_on()
    #mini_map.scroll_state = "on"
        
    clock = pygame.time.Clock()
    
    render_game_world = True
    toggle_mini_map = False
    
    
    ant_image = pygame.image.load("assets/ant.png").convert_alpha()
    ant_image_2 = pygame.image.load("assets/ant-blue.png").convert_alpha()
    leaf_image = pygame.image.load("assets/leaf.png").convert_alpha()
    base_image = pygame.image.load("assets/hut1.png").convert_alpha()
    base_image_2 = pygame.image.load("assets/hut1.png").convert_alpha()
    base_image_2 = pygame.transform.flip(base_image_2, 1, 0)
    #Let's make hut 1 for our little ants.
    base_1 = entities.Base(world, base_image, 1, (255,255,255))
    base_1.location = (global_data.NEST_POSITION)
    
    base_2 = entities.Base(world, base_image_2, 2, (255,255,255))
    base_2.location = (global_data.NEST_POSITION_2)
    
    world.add_entity(base_1)
    world.add_entity(base_2)
        
    for ant_no in xrange(global_data.ANT_COUNT):
        #Team 1
        ant = entities.Ant(world, ant_image, base_1, (255, 0, 0))
        ant.location = Vector2(randint(0, world.width), randint(0, world.height))
        ant.brain.set_state("exploring")
        world.add_entity(ant)
        #Team 2
        ant = entities.Ant(world, ant_image_2, base_2, (0, 0, 255))
        ant.location = Vector2(randint(0, world.width), randint(0, world.height))
        ant.brain.set_state("exploring")
        world.add_entity(ant)
    
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
        
        time_passed = clock.tick(60)
        
        if randint(1, 10) == 1:
            leaf = entities.Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, leaf.world.width), randint(0, leaf.world.height))
            world.add_entity(leaf)
            

        
        world.process(time_passed)
        if render_game_world:
            world.render(screen)
        print_fps(clock, screen)
        
        #Let's Draw the Mini_Map
        mini_map.render(world, screen)
        
        #the_background = pygame.surface.Surface((256, 170)).convert()
        #the_background.fill((0, 0, 0))
        #self.surface.blit(self.background, (0, 0))
        #screen.blit(the_background, (944, 598))
        
        #control_panel.render(screen, world)
        #conStrol_panel.render_base_stats(screen, world, base_1, 25)
        #control_panel.render_base_stats(screen, world, base_2, 100)
        


        pygame.display.update()
    
if __name__ == "__main__":    
    run()
    exit()
    

