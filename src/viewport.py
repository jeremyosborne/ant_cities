"""
An class for implementing a viewport.
"""

import pygame

class Viewport(pygame.Surface):
    """Extends pygame's surface class for managing multiple surfaces.
    
    The viewport class builds on the idea of a surface and provides a system
    to manage multiple surfaces that may or may not be visable on the screen.
    It is useful when an application manages multiple and independent
    on screen game components such as a mini-map, a command toolbar,
    or pop up windows that overlay onto the game screen.
    
    Viewport provides the following functionality:
    
    1.  Manages rendering order of the surfaces, i.e. viewports are layered
        and rendering order onto the final surface is important for end
        user viewing.
    2.  Manages user input such that user input is directed to the proper
        viewport to be acted upon.  This is based on mouse location, or
        definition of the viewport as exclusive or not.
        
    This class can manage routing of events such as mouse clicks and keyboard
    events.  This class will not manage mouse movements without clicks.
    
    """

    #  Class variables section.
    #  These class variables will be used in managing the rendering and event processing layers.
    #  Class methods will be used to manage the data.

    #  A List of all the surfaces.
    #  Purpose:  Can be iterated through for the following tasks:
    #  - Final rendering - blit the surfaces in the order defined by layer.
    #  - Find the right viewport the user input belongs to.

    # List to contain all the viewports.  Using a list instead of a dictionary
    # because I want to sort them based on layer.
    viewports = []    

    @classmethod
    def add_viewport(cls, viewport):
        """  Add a viewport to the tracking list.  """
        cls.viewports.append(viewport)
        #Sort list on layer.
        cls.sort_viewports()

    @classmethod
    def sort_viewports(cls):
        """  Sort viewports by layer for rendering and user input routing.  """
        cls.viewports.sort(key = lambda x: x.layer)
        
    @classmethod        
    def remove_viewport(cls, viewport):
        """  Delete viewport from list """
        cls.viewports.remove(viewport)

    @classmethod                
    def render_viewports(cls, main_surface):
        """  Render the viewports from layer 0 to highest layer.  """
        for i in cls.viewports:
            #Is it viewable?
            if i.is_visable:
                main_surface.blit(i.surface, ((i.x_right, i.y_down)))
                #This is for debug purposes.
                #print "Rendering:  " + i.description
    
    @classmethod
    def highest_layer(cls):
        """  Returns the current highest layer as integer.  Developers may
             call this function when creating a new window on screen """
        try:
            return cls.viewports[-1]._layer
        except:
            return -1

    #----------------------------------------------------------------------------#   
    def __init__(self, x_right=0, y_down=0, width=1024, height=768, scale=1, layer=0, is_visable=True):
        """Arguments assumed to be integers."""
        # The upper left anchor point of our viewport
        self.x_right = x_right
        self.y_down = y_down
        # The dimensions of our viewport as [width, height]
        # Assumed width and height are positive.
        self._width = width
        self._height = height
        # Scales relative to 1 as default.
        #Not used yet.
        self.scale = scale
        # The surface for this screen entity.
        self.surface = pygame.surface.Surface((self._width, self._height)).convert()
        # Layer, can be thought of as the sequence of blitting onto a layer.
        # 0 is the lowest layer.
        self._layer = layer
        #Should this be rendered?
        self.is_visable=is_visable
        #User defined description field.
        self.description = "Not defined"       
        # Add to viewport management list.
        self.add_viewport(self)
        # Rectangle area matching the actual screen area this viewport maps to.
        self.rect = pygame.Rect(self.x_right, self.y_down, self._width, self._height)
        
        #Proposed attribute to restrict the area to monitor for input.
        self.event_area = None
        #When visiable, no input should be passed below this layer.
        self.exclusive_mouse = False
        self.exclusive_keyboard = False
        
    @property
    def layer(self):
        """{int}  0 = lowest layer, no upper bound."""
        return self._layer
    
    @layer.setter
    def layer(self, value):
        """  Set's layer value and sorts the viewports on this value.  """
        self._layer = value
        Viewport.sort_viewports()

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self.resize()
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self.resize_surface()
        
    def resize_surface(self, width, height):
        """ Resizes the surface, called when width or height is changed. """
        self.surface = pygame.surface.Surface((self._width, self._height)).convert()
        self.set_rectangle_area()
        
    def set_rectangle_area(self):
        self.rect = pygame.Rect(self.x_right, self.y_down, self._width, self._height)
        
    
    #Render this Screen Entity into whatever surface is passed in.    
    def render(self, main_surface):
        main_surface.blit(self.surface, ((self.x_right, self.y_down)))

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
        return (coord[0]-self.x_right, coord[1]-self.y_down)





        
if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((1024,768), 0, 32)
        
    print "Testing..."
    v = Viewport()
    print "Initial viewport width: %s" % v.width
    print "Viewport layer: %s" % v.layer
    print "Changing Viewport layer number to 10"
    v.layer = 10
    print "Viewport layer: %s" % v.layer
    
    print "Left anchor: %s" % v.y_down
    #print "Right anchor: %s" % v.right
    print "Changing left anchor point by 100."
    v.y_down = 100
    print "Left anchor: %s" % v.y_down
    #print "Right anchor: %s" % v.right

    print "Initial viewport height: %s" % v.height
    print "Top anchor: %s" % v.x_right
    #print "Bottom anchor: %s" % v.bottom
    print "Changing top anchor point by 100."
    v.x_right = 100
    print "Top anchor: %s" % v.x_right
    #print "Bottom anchor: %s" % v.bottom
    