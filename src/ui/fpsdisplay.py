import pygame
from ui.pygameview import PygameView

class FPSDisplay(PygameView):
    """Display frames per second.
    """
    def __init__(self, x, y, controller):
        PygameView.__init__(self, x, y, 125, 20, 0, controller)
        
        self.font = pygame.font.SysFont("arial", 16)

        # Set transparency color.
        self.surface.set_colorkey((255, 255, 255))
        
    def draw_view(self, surface):
        
        # Clear the surface.
        self.surface.fill((255, 255, 255))    

        label = self.font.render("fps: %s" % self.controller.fps, True, (0, 0, 0))
        self.surface.blit(label, (0, 0))

        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))
