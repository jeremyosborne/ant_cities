import pygame
import ui.viewport as viewport

class FPSDisplay(viewport.Viewport):
    def __init__(self, x, y, controller):
        viewport.Viewport.__init__(self, x, y, 125, 20)
        self.font = pygame.font.SysFont("arial", 16)
        self.background = pygame.surface.Surface((125, 20)).convert()
        self.background.fill((255, 255, 255))
        # Make it such that when the surface is blitted on something else,
        # the background is transparent.
        self.surface.set_colorkey((255, 255, 255))
        
        self.controller = controller
        
    def update(self):
        
        fps = self.controller.game_simulation.clock.get_fps()

        # Clear the surface.
        self.surface.blit(self.background, (0, 0))    

        label = self.font.render(str(fps), True, (0, 0, 0))
        self.surface.blit(label, (0, 0))
