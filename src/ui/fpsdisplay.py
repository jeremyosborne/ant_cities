import pygame
from common.ui.pygameview import PygameView

class FPSDisplay(PygameView):
    """Display frames per second.
    """
    def subclass_init(self, **kwargs):
        self.font = pygame.font.SysFont("arial", 16)
        
        # Set a default width if width is not set.
        self.width = self.width or 250
        self.height = self.height or 20

        # Set transparency color.
        self.surface.set_colorkey((255, 255, 255))
    
    def clear(self):
        self.surface.fill((255, 255, 255))    
        
    def draw(self, surface):
        label = self.font.render("fps: %s" % self.controller.fps, True, (0, 0, 0))
        self.surface.blit(label, (0, 0))

        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))
