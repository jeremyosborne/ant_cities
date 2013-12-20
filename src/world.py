'''
Created on Jun 19, 2013

@author: john
'''

import time
from collections import Counter

from random import randint
from pymunk.vec2d import Vec2d

from commonmath import random_radial_offset

from entities.base import Base
from entities.leaf import Leaf
import globaldata
import spatialengine

class World(object):
        
    def __init__(self, width, height, imageassets):
        """Notes:
        
        imageassets {AssetCache} Image cache.
        """
        
        #The size of the world for x and y
        self.width = width
        self.height = height
        
        # Dictionary of all the entities
        self.entities = {}

        self.spatial_index = spatialengine.SpatialEngine(self.width, self.height)

        self.time_born = time.time()
        # Various score counters. 
        # Short term solution to cut down on counting variables.
        self.stats = Counter()
        
        #-----------------------------------------------------------------------
        #Setting up initial entity elements.
        #-----------------------------------------------------------------------

        # Generate bases.
        self.base_1 = Base(self, 1, "Red Ants")
        self.base_1.location = globaldata.NEST_POSITION
        self.add_entity(self.base_1)
        
        self.base_2 = Base(self, 2, "Blue Ants")
        self.base_2.location = globaldata.NEST_POSITION_2
        self.add_entity(self.base_2)
        
        # Generate ants.
        for _ in xrange(globaldata.ANT_COUNT):
            # Randomize starting position.
            startxy = random_radial_offset(100)
            # Red team (Team 1)
            ant = self.base_1.create_entity("ant", startxy)
            self.add_entity(ant)
            # Blue team (Team 2)
            ant = self.base_2.create_entity("ant", startxy)
            self.add_entity(ant)


    #------------------------------------------------------------------------
    #Done setting up initial entity elements.
    #------------------------------------------------------------------------
        
    def add_entity(self, entity):   #The entity is whatever game entity object is being passed in.        
        self.entities[entity.id] = entity
        # Count vs. net.
        self.stats[entity.name] += 1
        self.stats[entity.name+"-added"] += 1
        
    def remove_entity(self, entity):
        del self.entities[entity.id]
        entity.delete()
        self.spatial_index.remove(entity)

        # Count vs. net.
        self.stats[entity.name] -= 1
        self.stats[entity.name+"-removed"] += 1

                
    def get(self, entity_id):
        """Retrieve an entity by id.
        """
        return self.entities.get(entity_id)
        
    def process(self, time_passed):
                
        time_passed_seconds = time_passed / 1000.0
        
        #Here's our chance to throw in a new leaf
        if randint(1, 20) == 1:
            leaf = Leaf(self)
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
