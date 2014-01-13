import pygame
import ui.viewport as viewport

class FPSDisplay(viewport.Viewport):
    """Display frames per second.
    """
    def __init__(self, x, y, controller):
        viewport.Viewport.__init__(self, x, y, 125, 20)
        
        self.font = pygame.font.SysFont("arial", 16)

        # Set transparency color.
        self.surface.set_colorkey((255, 255, 255))
        
        self.controller = controller
        
    def update(self):
        
        # Clear the surface.
        self.surface.fill((255, 255, 255))    

        label = self.font.render("fps: %s" % self.controller.fps, True, (0, 0, 0))
        self.surface.blit(label, (0, 0))
