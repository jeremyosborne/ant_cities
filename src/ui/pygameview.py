import pygame
from ui.view import View, PositionableMixin, ScalableMixin
from events import EventSubscriber



class PygameDisplay(View, EventSubscriber):
    """Special view representing the main display surface in Pygame.
    
    This should be the outermost view and all views should be nested within.
    """
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):
        # Windowed view.
        self.surface = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        # Full screen mode.
        #screen = pygame.display.set_mode(globaldata.SCREEN_SIZE, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

        self.rect = pygame.Rect(x, y, width, height) 

        # Initialize the view and call the subclass init.
        super(PygameDisplay, self).__init__(x, y, width, height, z, controller, **kwargs)

    def draw_view(self, surface):
        """Refresh the view of the game.
        """
        pygame.display.flip()



class PygameView(View, EventSubscriber, PositionableMixin, ScalableMixin):
    """A View made for use with Pygame.
    """
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):
        # Pygame specific surface.
        self.surface = pygame.surface.Surface((width, height)).convert()

        # Pygame specific helper.
        self.rect = pygame.Rect(x, y, width, height)
        
        # Initialize the view and call the subclass init.
        super(PygameView, self).__init__(x, y, width, height, z, controller, **kwargs)

