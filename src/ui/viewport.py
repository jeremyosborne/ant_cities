"""
An class for implementing a viewport.
"""

import pygame

class Viewport(pygame.Surface):
    """Extends pygame's surface class for managing UI.    
    """
    
    def __init__(self, x=0, y=0, width=1024, height=768):
        """Arguments assumed to be integers."""
        # The upper left anchor point.
        self.x = x
        self.y = y
        # The dimensions of our viewport.
        self.width = width
        self.height = height
        # All visual updates blitted here. Surface then blitted onto screen.
        self.surface = pygame.surface.Surface((self.width, self.height)).convert()
        # Rectangle area matching the actual screen area this viewport maps to.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, **kwargs):
        """Each view will be asked to update prior to rendering.
        
        Views must accept all arguments, even the ones they don't want.
        """
        pass
        
    def render(self, main_surface):
        main_surface.blit(self.surface, ((self.x, self.y)))

    def screenxy_to_relativexy(self, coord):
        """Convert a universal device coordinate to a relative xy coordinate.

        !!!!!!!!!!!!
        NOTE: Not the same as the view.py screenxy_to_relativexy, but should
        not require changing when code is switched over.
        !!!!!!!!!!!!
        
        coord {Indexable} An integer indexable item where [0] is the x 
        coordinate and [1] is the y coordinate equivalent. Coord is assumed to
        be an untranslated coordinate.
        
        returns {tuple} an indexable coordinate relative to this rect.
        """
        return (coord[0]-self.x, coord[1]-self.y)





        
