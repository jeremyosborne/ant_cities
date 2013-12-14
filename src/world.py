'''
Created on Jun 19, 2013

@author: john
'''

import time
import pygame
from pygame.locals import *

from random import randint
from pymunk.vec2d import Vec2d

from entities.ant import Ant
from entities.base import Base
from entities.leaf import Leaf
import globaldata
import spatialengine

class World(object):
        
    def __init__(self, x, y, w, h, imageassets):
        """Notes:
        
        imageassets {AssetCache} Image cache.
        """
        
        #The size of the world for x and y
        self.width = x
        self.height = y
        
        self.viewable_width = w
        self.viewable_height = h
        
        # Dictionary of all the entities
        self.entities = {}

        self.spatial_index = spatialengine.SpatialEngine(self.width, self.height)

        self.time_born = time.time()
        #Initialize counters
        self.base_count = 0
        self.leaf_born = 0  #Total number of leaves created.
        self.leaf_expired = 0 #Total number of leaves that died without being picked up.
        self.leaf_world_count = 0 #Total number of leaves in the world.
        
        
#-----------------------------------------------------------------------
#Setting up initial entity elements.
#-----------------------------------------------------------------------

        self.leaf_image = imageassets.get("leaf")
        #Let's make hut 1 for our little ants.
        self.base_1 = Base(self, imageassets.get("hut"), 1, (255, 255, 0), "Red Ants")
        self.base_1.location = (globaldata.NEST_POSITION)
        #Let's make hut 2 for our little ants.
        self.base_2 = Base(self, pygame.transform.flip(imageassets.get("hut"), 1, 0), 2, (255, 255, 0), "Blue Ants")
        self.base_2.location = (globaldata.NEST_POSITION_2)
    
        self.add_entity(self.base_1)
        self.add_entity(self.base_2)
        
        for ant_no in xrange(globaldata.ANT_COUNT):
            #Team 1
            ant = Ant(self, imageassets.get("red-ant"), self.base_1, (255, 0, 0))
            ant.location = Vec2d(randint(0, self.width), randint(0, self.height))
            ant.brain.set_state("exploring")
            self.add_entity(ant)
            #Team 2
            ant = Ant(self, imageassets.get("blue-ant"), self.base_2, (0, 0, 255))
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
