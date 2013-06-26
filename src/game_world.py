'''
Created on Jun 19, 2013

@author: john
'''

import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

import ui_elements
import entities
import statemachines
import global_data
import viewport

class World(object):
        
    def __init__(self, x, y):
        
        #The size of the world for x and y
        self.width = x
        self.height = y
        
        self.entities = {}    #Dictionary of all the entities
        self.entity_id = 0
        #viewport is the screen entity that contains the view of the game world.
        self.viewport = ui_elements.World_Viewport(self.width, self.height)
        self.viewport.description = "Game world viewport."
        
#-----------------------------------------------------------------------
#Setting up initial entity elements.
#-----------------------------------------------------------------------

        self.ant_image = pygame.image.load("assets/ant.png").convert_alpha()
        self.ant_image_2 = pygame.image.load("assets/ant-blue.png").convert_alpha()
        self.leaf_image = pygame.image.load("assets/leaf.png").convert_alpha()
        self.base_image = pygame.image.load("assets/hut1.png").convert_alpha()
        self.base_image_2 = pygame.image.load("assets/hut1.png").convert_alpha()
        self.base_image_2 = pygame.transform.flip(self.base_image_2, 1, 0)
        #Let's make hut 1 for our little ants.
        self.base_1 = entities.Base(self, self.base_image, 1, (255,255,255))
        self.base_1.location = (global_data.NEST_POSITION)
        #Let's make hut 2 for our little ants.
        self.base_2 = entities.Base(self, self.base_image_2, 2, (255,255,255))
        self.base_2.location = (global_data.NEST_POSITION_2)
    
        self.add_entity(self.base_1)
        self.add_entity(self.base_2)
        
        for ant_no in xrange(global_data.ANT_COUNT):
            #Team 1
            ant = entities.Ant(self, self.ant_image, self.base_1, (255, 0, 0))
            ant.location = Vector2(randint(0, self.width), randint(0, self.height))
            ant.brain.set_state("exploring")
            self.add_entity(ant)
            #Team 2
            ant = entities.Ant(self, self.ant_image_2, self.base_2, (0, 0, 255))
            ant.location = Vector2(randint(0, self.width), randint(0, self.height))
            ant.brain.set_state("exploring")
            self.add_entity(ant)
            
#------------------------------------------------------------------------
#Done setting up initial entity elements.
#------------------------------------------------------------------------
        
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
        
        #Here's our chance to throw in a new leaf
        
        if randint(1, 10) == 1:
            leaf = entities.Leaf(self, self.leaf_image)
            leaf.location = Vector2(randint(0, leaf.world.width), randint(0, leaf.world.height))
            self.add_entity(leaf)
                    
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            
    def render(self):
        
        #Prepares for this frame.  Clears the background, etc.
        self.viewport.prepare_new_frame()
        
        #Render each entity onto the framebuffer.
        for entity in self.entities.itervalues():
            entity.render(self.viewport)
        #Render the framebuffer onto viewport surface.    
        self.viewport.finalize_image()
            
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