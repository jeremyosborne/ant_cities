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
import screen_entity


      
class ControlPanel(object):
    
    def __init__(self, world):
        
        self.font = pygame.font.SysFont("arial", 16);
        screen_width, screen_height = global_data.screen_size
        panel_height = 256
        panel_starting_position = screen_height - panel_height
        size_of_world_stats = 280
        size_of_team_stats = 445
        
        #Draw static elements on the control panel.
        #Horizontal Line
        pygame.draw.line(world.background, (0, 0, 255), (0, panel_starting_position), (screen_width, panel_starting_position), 5)
        #First deliminator
        pygame.draw.line(world.background, (0, 0, 255), (size_of_world_stats, panel_starting_position), (size_of_world_stats, screen_height), 5)
        #second deliminator
        pygame.draw.line(world.background, (0, 0, 255), (740, 512), (740, 768), 5)
        
        font = pygame.font.SysFont("arial", 16);
        label = font.render("World Statistics", True, (0, 0, 0))
        world.background.blit(label, (5, screen_height - panel_height + 7))
        label = font.render("Total Number of Ants: ", True, (0, 0, 0))
        world.background.blit(label, (5, screen_height - panel_height + 32))
        label = font.render("Number of Leaves on Screen: ", True, (0, 0, 0))
        world.background.blit(label, (5, screen_height - panel_height + 57))
        label = font.render("Number of Returned Leaves: ", True, (0, 0, 0))
        world.background.blit(label, (290, screen_height - panel_height + 32))
        label = font.render("Number of Leaves in Base: ", True, (0, 0, 0))
        world.background.blit(label, (290, screen_height - panel_height + 57))       
        label = font.render("Number of Food Units: ", True, (0, 0, 0))
        world.background.blit(label, (290, screen_height - panel_height + 82))
        label = font.render("Team 1      Team 2", True, (0, 0, 0))
        world.background.blit(label, (525, screen_height - panel_height + 7))
        label = font.render("MiniMap", True, (0, 0, 0))
        world.background.blit(label, (850, screen_height - panel_height + 7))
        #Other Stuff
        self.ant_location = (225, screen_height - panel_height + 32)
        self.leaf_location = (225, screen_height - panel_height + 57)
        self.leaf_returned_location = (520, screen_height - panel_height + 32)
        self.leaf_in_base_location = (520, screen_height - panel_height + 57)
        self.food_units_location = (520, screen_height - panel_height + 82)
        
    #Let's render all the interesting things about the world        
    def render(self, surface, world):
  
        label = self.font.render(str(world.count("ant")), True, (0, 0, 0))
        surface.blit(label, self.ant_location)
        label = self.font.render(str(world.count("leaf")), True, (0, 0, 0))
        surface.blit(label, self.leaf_location)   
    
    def render_base_stats(self, surface, world, base, offset):
        label = self.font.render(str(base.leaves_returned), True, (0, 0, 0))
        x, y = self.leaf_returned_location
        surface.blit(label, (x + offset, y))
        label = self.font.render(str(base.leaves), True, (0, 0, 0))
        x, y = self.leaf_in_base_location
        surface.blit(label, (x + offset, y))
        label = self.font.render(str(base.food_units), True, (0, 0, 0))
        x, y = self.food_units_location
        surface.blit(label, (x + offset, y))
        

class World(object):
    
    def __init__(self, x, y):
        
        #The size of the world for x and y
        self.width = x
        self.height = y
        
        self.entities = {}    #Dictionary of all the entities
        self.entity_id = 0
        #viewport is the screen entity that contains the view of the game world.
        self.viewport = screen_entity.World_Screen_Entity(self.width, self.height)
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
    mini_map = screen_entity.Mini_Map(1200-256, 768-170, 256, 170, global_data.world_size_x, global_data.world_size_y)

    
    clock = pygame.time.Clock()
    
    render_game_world = True
    toggle_mini_map = False
    
    
    ant_image = pygame.image.load("assets/ant.png").convert_alpha()
    ant_image_2 = pygame.image.load("assets/ant-blue.png").convert_alpha()
    leaf_image = pygame.image.load("assets/leaf.png").convert_alpha()
    spider_image = pygame.image.load("assets/spider.png").convert_alpha()
    base_image = pygame.image.load("assets/hut1.png").convert_alpha()
    base_image_2 = pygame.image.load("assets/hut1.png").convert_alpha()
    base_image_2 = pygame.transform.flip(base_image_2, 1, 0)
    seth_image = pygame.image.load("assets/seth.png")
    sri_image = pygame.image.load("assets/sri.png")
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
                if event.key == K_s:
                    seth = entities.Seth(world, seth_image)
                    seth.location = Vector2(-50, randint(0, h))
                    seth.brain.set_state("exploring")
                    world.add_entity(seth)
                if event.key == K_z:
                    sri = entities.Sri(world, sri_image) 
                    world.add_entity(sri)
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
                if event.key == K_m:   #Toggle mini-map
                    if toggle_mini_map:
                        toggle_mini_map = False
                    else:
                        toggle_mini_map = True
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
    

