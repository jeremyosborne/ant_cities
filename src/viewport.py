"""
An class for implementing a viewport.
"""

import pygame
from pygame.locals import *

import global_data


class Viewport(pygame.Surface):
    """Manages various viewport abstractions."""
    

    #Class variables section.
    #These class variables will be used in managing the rendering and event processing layers.
    #Class methods will be used to manage the data.

    #A List of all the surfaces.
    #Purpose:  Can be iterated through for the following tasks:
    #  - Final rendering - blit the surfaces in the order defined by layer.
    #  - Find the surface that belongs to a coordinate belongs to based on
    #    the highest layer.
    
    def __init__(self, x_right=0, y_down=0, width=1024, height=768, scale=1, layer=0, is_visable=True):
        """Arguments assumed to be integers."""
        # The upper left anchor point of our viewport
        self.x_right = x_right
        self.y_down = y_down
        # The dimensions of our viewport as [width, height]
        # Assumed width and height are positive.
        self.size = [width, height]
        self.width = width
        self.height - height
        # Scales relative to 1 as default.
        self.scale = scale
        #The surface for this screen entity.
        self.surface = pygame.surface.Surface(self.size).convert()
        #Layer, can be though of as the sequence of blitting.  0 is the lowest layer.
        self.layer = layer
        #Should this be rendered?
        self.is_visable=is_visable


        
#    @property
#    def top(self):
#        """{int} The relative top coordinate offset."""
#        return self.anchor[1]
    
#    @top.setter
#    def top(self, value):
#        self.anchor[1] = value
    
 #   @property
 #   def left(self):
 #       """{int} The relative left coordinate offset."""
 #       return self.anchor[0]
    
#    @left.setter
#    def left(self, value):
#        self.anchor[0] = value
    
#    @property
#    def right(self):
#        """{int} The relative right coordinate (offset + width)."""
#        return self.anchor[0] + self.size[0]

#    @property
#    def bottom(self):
#        """{int} The relative bottom coordinate (offset + height)."""
#        return self.anchor[1] + self.size[1]
    
    @property
    def width(self):
        return self.size[0]
    
    @width.setter
    def width(self, value):
        self.size[0] = value
    
    @property
    def height(self):
        return self.size[1]
    
    @height.setter
    def height(self, value):
        self.size[1] += value

    #Render this Screen Entity into whatever surface is passed in.    
    def render(self, main_surface):
        main_surface.blit(self.surface, ((self.x_right, self.y_down)))


if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((1024,768), 0, 32)
        
    print "Testing..."
    v = Viewport()
    print "Initial viewport width: %s" % v.width
    print "Left anchor: %s" % v.y_down
    print "Right anchor: %s" % v.right
    print "Changing left anchor point by 100."
    v.y_down = 100
    print "Left anchor: %s" % v.y_down
    print "Right anchor: %s" % v.right

    print "Initial viewport height: %s" % v.height
    print "Top anchor: %s" % v.x_right
    print "Bottom anchor: %s" % v.bottom
    print "Changing top anchor point by 100."
    v.x_right = 100
    print "Top anchor: %s" % v.x_right
    print "Bottom anchor: %s" % v.bottom
