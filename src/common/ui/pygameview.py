"""pygame flavored implementation of Views.
"""

import pygame
from common.ui.view import View, PositionableMixin, ScalableMixin
from common.events import EventSubscriber



class PygameDisplay(View, EventSubscriber):
    """Special view representing the main display surface in Pygame.
    
    This should be the outermost view and all views should be nested within.
    """
    def __init__(self, width=0, height=0):
        # Initialize the view and call the subclass init.
        super(PygameDisplay, self).__init__(width=width, height=height)

        # Windowed view.
        self.surface = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        # Full screen mode.
        #screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

    def draw(self, surface):
        """Refresh the view of the game.
        """
        pygame.display.flip()

    def events_sub(self):
        # Not a PygameView subclass. Need to implement PygameView specific methods.
        pass
    
    def events_unsub(self):
        # Not a PygameView subclass. Need to implement PygameView specific methods.
        pass
    


class PygameView(View, EventSubscriber, PositionableMixin, ScalableMixin):
    """A View made for use with Pygame.
    """
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):        
        # Initialize the view and call the subclass init.
        super(PygameView, self).__init__(x, y, width, height, z, controller, **kwargs)

        # self.surface init.
        self.init_surface()

        # Also call events_sub() automatically.
        self.events_sub()

    @View.width.setter
    def width(self, value):
        """Override and resize on width change.
        """
        self._width = value
        self.init_surface()

    @View.height.setter
    def height(self, value):
        """Override and resize on height change.
        """
        self._height = value
        self.init_surface()

    def init_surface(self, width=None, height=None):
        """Called to create the surface.
        
        the dimensions of the surface can be overridden, but will default to
        the width and height of the view.
        """
        height = height if height is not None else self.height
        width = width if width is not None else self.width
        self.surface = pygame.surface.Surface((width, height)).convert()

    def clear(self):
        """Default clear method.
        """
        self.surface.fill((0, 0, 0))

    def draw(self, surface):
        """Default draw method.
        """
        surface.blit(self.surface, ((self.x, self.y)))

    def events_sub(self):
        """Views should override and place all event subscriptions in this
        method.
        
        Outside controllers may use this to (re)add events in the event that
        their listeners need to be temporarily suspended.
        """
        pass
    
    def events_unsub(self):
        """Views should override and place a uniform event unsub from this
        method.
        
        Outside controllers may use this to remove events in the event that
        their listeners need to be temporarily suspended.
        """
        self.unsubfrom()
    