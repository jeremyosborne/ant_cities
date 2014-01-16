import pygame
from ui.view import View, PositionableMixin, ScalableMixin
from events import EventSubscriber



class PygameDisplay(View, EventSubscriber):
    """Special view representing the main display surface in Pygame.
    
    This should be the outermost view and all views should be nested within.
    """
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):
        # Set the title.
        pygame.display.set_caption(controller.game_engine.globaldata.GAME_TITLE)

        # Windowed view.
        self.surface = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        # Full screen mode.
        #screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

        self.rect = pygame.Rect(x, y, width, height) 

        # Initialize the view and call the subclass init.
        super(PygameDisplay, self).__init__(x, y, width, height, z, controller, **kwargs)

        # mimic PygameView... just in case.
        self.events_sub()

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
        # Pygame specific surface.
        self.surface = pygame.surface.Surface((width, height)).convert()

        # Pygame specific helper.
        # TODO: I don't think this is needed. Shoul remove if not.
        self.rect = pygame.Rect(x, y, width, height)
        
        # Initialize the view and call the subclass init.
        super(PygameView, self).__init__(x, y, width, height, z, controller, **kwargs)
        
        # Also call events_sub() automatically.
        self.events_sub()

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
    