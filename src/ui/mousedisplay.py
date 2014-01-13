import pygame
import ui.viewport as viewport

class MouseDisplay(viewport.Viewport):
    """Display the translation of mouse device coordinates to mouse game world
    coordinates.
    """
    def __init__(self, x, y, controller):
        viewport.Viewport.__init__(self, x, y, 250, 20)

        self.font = pygame.font.SysFont("arial", 16)
        
        # Set transparency color.
        self.surface.set_colorkey((255, 255, 255))
        
        self.controller = controller
        
    def update(self):
        
        # Clear the surface.
        self.surface.fill((255, 255, 255))

        game_world_x, game_world_y = self.controller.mouse_worldxy
        text = "Mouse coords: (%d, %d)" % (game_world_x, game_world_y)
        font = self.font.render(text, True, (0, 0, 0))
        self.surface.blit(font, (0, 0))
