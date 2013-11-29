'''
Created on Jun 19, 2013

@author: john
'''

import time
import pygame
from pygame.locals import *

from random import randint
from pymunk.vec2d import Vec2d

from ui.world_viewport import World_Viewport
from entities.ant import Ant
from entities.base import Base
from entities.leaf import Leaf
import global_data
import spatial_engine

class World(object):
        
    def __init__(self, x, y, w, h):
        
        #The size of the world for x and y
        self.width = x
        self.height = y
        
        self.viewable_width = w
        self.viewable_height = h
        
        self.entities = {}    #Dictionary of all the entities
        #viewport is the screen entity that contains the view of the game world.
        self.viewport = World_Viewport(self.width, self.height, self.viewable_width, self.viewable_height)
        self.viewport.description = "Game world viewport."
        
        self.spatial_index = spatial_engine.SpatialEngine(self.width, self.height)

        self.time_born = time.time()
        #Initialize counters
        self.base_count = 0
        self.leaf_born = 0  #Total number of leaves created.
        self.leaf_expired = 0 #Total number of leaves that died without being picked up.
        self.leaf_world_count = 0 #Total number of leaves in the world.
        
        
#-----------------------------------------------------------------------
#Setting up initial entity elements.
#-----------------------------------------------------------------------

        self.ant_image = pygame.image.load("assets/red-ant.png").convert_alpha()
        self.ant_image_2 = pygame.image.load("assets/blue-ant.png").convert_alpha()
        self.leaf_image = pygame.image.load("assets/leaf.png").convert_alpha()
        self.leaf_image2 = pygame.image.load("assets/leaf2.png").convert_alpha()
        self.base_image = pygame.image.load("assets/hut1.png").convert_alpha()
        self.base_image_2 = pygame.image.load("assets/hut1.png").convert_alpha()
        self.base_image_2 = pygame.transform.flip(self.base_image_2, 1, 0)
        #Let's make hut 1 for our little ants.
        self.base_1 = Base(self, self.base_image, 1, (255, 255, 0), "Red Ants")
        self.base_1.location = (global_data.NEST_POSITION)
        #Let's make hut 2 for our little ants.
        self.base_2 = Base(self, self.base_image_2, 2, (255, 255, 0), "Blue Ants")
        self.base_2.location = (global_data.NEST_POSITION_2)
    
        self.add_entity(self.base_1)
        self.add_entity(self.base_2)
        
        for ant_no in xrange(global_data.ANT_COUNT):
            #Team 1
            ant = Ant(self, self.ant_image, self.base_1, (255, 0, 0))
            ant.location = Vec2d(randint(0, self.width), randint(0, self.height))
            ant.brain.set_state("exploring")
            self.add_entity(ant)
            #Team 2
            ant = Ant(self, self.ant_image_2, self.base_2, (0, 0, 255))
            ant.location = Vec2d(randint(0, self.width), randint(0, self.height))
            ant.brain.set_state("exploring")
            self.add_entity(ant)
            

            
#------------------------------------------------------------------------
#Done setting up initial entity elements.
#------------------------------------------------------------------------
        
    def add_entity(self, entity):   #The entity is whatever game entity object is being passed in.        
        self.entities[entity.id] = entity
        
    def remove_entity(self, entity):
        # Should this be triggered by the ant delete for now?
        self.spatial_index.remove(entity)
        #execute triggers for deleted item.
        entity.delete()
        del self.entities[entity.id]
                
    def get(self, entity_id):
        return self.entities.get(entity_id)
        
    def process(self, time_passed):
                
        time_passed_seconds = time_passed / 1000.0
        
        #Here's our chance to throw in a new leaf
        
        if randint(1, 20) == 1:
            leaf = Leaf(self, self.leaf_image)
            leaf.location = Vec2d(randint(0, leaf.world.width), randint(0, leaf.world.height))
            self.add_entity(leaf)
                    
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            
    def render(self, draw=True):
        """Update the game world.
        
        [draw] {bool} Override to allow temporary non-drawing.
        """
        if not draw:
            return
        
        #Prepares for this frame.  Clears the background, etc.
        self.viewport.prepare_new_frame()
        
        #Using the spatial index to determine what to render.  Let's not use the index if we're completely zoomed out. 
        if self.viewport.zoom_area_width != self.width:
            #Calculate the range.
            if self.viewport.zoom_area_width > self.viewport.zoom_area_height:
                the_range = self.viewport.zoom_area_width/2
            else:
                the_range = self.viewport.zoom_area_height/2
                 
            entity_list_in_range = self.spatial_index.find_all_in_range((self.viewport.world_viewable_center_x, self.viewport.world_viewable_center_y), the_range)
    
            #Render each entity onto the framebuffer.
            for entity in entity_list_in_range:
                entity[0].render(self.viewport)
        else:
            for entity in self.entities.itervalues():
                entity.render(self.viewport)

            
    def get_close_entity(self, entity, name, the_range=100.):
        closest_entity, distance = self.spatial_index.find_closest(entity.location, 
                                                                   the_range, 
                                                                   validate=lambda e: e.name == name and e != entity)
        return closest_entity

    def count(self, name):
        entity_count = 0
        for entity in self.entities.itervalues():
            if entity.name == name:
                entity_count += 1
        return entity_count