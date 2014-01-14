import pygame
from ui.view import View
from events import EventSubscriber

class PygameView(View, EventSubscriber):
    """A View made for use with Pygame.
    """
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):
        # Pygame specific surface.
        self.surface = pygame.surface.Surface((width, height)).convert()

        # Pygame specific helper.
        self.rect = pygame.Rect(x, y, width, height)
        
        # Initialize the view and call the subclass init.
        super(PygameView, self).__init__(x, y, width, height, z, controller, **kwargs)
        