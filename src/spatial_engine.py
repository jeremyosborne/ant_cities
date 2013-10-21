'''
Created on Oct 20, 2013

@author: john
'''

import pymunk
from pymunk.vec2d import Vec2d

#For testing
import pygame
from pygame.locals import *
import game_world
import entities
import statemachines
import global_data
import viewport
import ui_elements
import sys
import os
from random import randint, choice



class spatial_engine(object):
    '''
    classdocs
    '''


    def __init__(self, world_size_x, world_size_y):
        '''
        Constructor
        '''
        #Size for X and Y for a grid element (cell.)
        self.cell_size = 100
        
        #Create the dictionary.
        self.spatial_index = {}
        
        #Initialize the dictionary and create the empty lists.
        for i in range (0, world_size_x / 100+1):
            for j in range (0, world_size_y / 100+1):
                self.spatial_index[i,j] = []
          
    def which_cell(self, x, y):
        x = x / self.cell_size
        y = y / self.cell_size
        return (x, y)
    
    def which_cells_to_search(self, entity, the_range):
        x, y = entity.location
        #Determine the area we should be looking at.
        x1 = int((x + the_range) / self.cell_size)
        x2 = int((x - the_range) / self.cell_size)
        y1 = int((y + the_range) / self.cell_size)
        y2 = int((y - the_range) / self.cell_size)
        
        cell_list = []
        
        #Build the list of cells that match the area.
        for i in range (x2, x1):
            for j in range (y2, y1):
                if self.spatial_index.has_key((i,j)):
                    #Valid cell to search.
                    cell_list.append((i,j))
        return(cell_list)    
              
    def insert(self, entity):
        x, y = entity.location
        x, y = self.which_cell(int(x), int(y))
        self.spatial_index[x,y].append(entity)
        
    def remove(self, entity):
        x, y = entity.location
        x, y = self.which_cell(int(x), int(y))
        self.spatial_index[x,y].remove(entity)
    
    def update(self, entity):
        #I don't think I need this one afterall and am doiong this work
        #inside the game_world class whenever location is updated.
        pass
    
    def find_closest(self, entity, the_range, name = "Any"):

        cell_list = self.which_cells_to_search(entity, the_range)
        closest_entity = None
        closest_distance = 200000000
        
        #x, y = entity.location
        #x, y = self.which_cell(int(x), int(y))
        
        #print "cell_list we're going to search.", cell_list
        #print "looking for: ", name
        if name == "Any":
            for cell in cell_list:
                for entity_in_cell in self.spatial_index[cell]: 
                    if entity_in_cell != entity:
                        distance = entity_in_cell.location.get_distance(entity.location)
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_entity = entity_in_cell
        else:
            for cell in cell_list:
                for entity_in_cell in self.spatial_index[cell]: 
                    if entity_in_cell != entity:
                        distance = entity_in_cell.location.get_distance(entity.location)
                        if distance < closest_distance and entity_in_cell.name == name:
                            closest_distance = distance
                            closest_entity = entity_in_cell      

        #print "Closest distance:" , closest_distance        
        if closest_distance <= the_range:
            return (closest_entity, closest_distance)
        else:
            return None, 0                

    
                
    def whats_in_range(self, entity):
        ''' Returns list of all entities in range. '''
        pass
    
    
    
if __name__ == "__main__":
    
    #Normal pygame window mode.
    #screen = pygame.display.set_mode(global_data.screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
    #world = game_world.World(global_data.world_size_x, global_data.world_size_y, global_data.screen_size_x, global_data.screen_size_y)
        
    #leaf_image = pygame.image.load("assets/leaf.png").convert_alpha()
    
    spatial_index = spatial_engine(global_data.world_size_x, global_data.world_size_y)
    world = "Nothing"
    leaf_image = "Nothing"
    leaf = entities.Leaf(world, leaf_image)
    leaf.location = Vec2d(250, 350)
    leaf2 = entities.Leaf(world, leaf_image)
    leaf2.location = Vec2d(351, 451)
    
    spatial_index.insert(leaf)
    spatial_index.insert(leaf2)
    print "Contents of cell 2,3:"
    print (spatial_index.spatial_index[2, 3])
    
    closest = spatial_index.find_closest(leaf, 100)
    print "Closest to leaf:", leaf, " is ", closest
    
    spatial_index.remove(leaf)
    print "Contents of cell 2,3:"
    print (spatial_index.spatial_index[2, 3])
    
    print spatial_index.which_cell(200, 300)


    print "Spatial Index Contents:"
    print spatial_index.spatial_index
    
    print "Doing benchmark insert."
    for leaf_no in xrange(10000):
        #Team 1
        leaf3 = entities.Leaf(world, leaf_image)
        leaf3.location = Vec2d(randint(0,global_data.world_size_x), randint(0, global_data.world_size_y))
        spatial_index.insert(leaf3)
            
    print "Doing benchmark search"
    for i in xrange(10000):
        closest, distance = spatial_index.find_closest(leaf, 100)
        
    print "Run complete."
    print closest, distance