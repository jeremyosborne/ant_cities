import pygame
import ui.viewport as viewport

class MouseDisplay(viewport.Viewport):
    """Display the mouse coordinates on the screen.
    """
    def __init__(self, x_right=5, y_down=5):
        viewport.Viewport.__init__(self, x_right, y_down, 250, 20, 1, 10, True)

        self.font = pygame.font.SysFont("arial", 16)
        self.background = pygame.surface.Surface((250, 20)).convert()
        self.background.fill((255, 255, 255))
        # Make it such that when the surface is blitted on something else,
        # the background is transparent.
        self.surface.set_colorkey((255, 255, 255))
        
    def update(self, worldviewport):
        # Clear the surface.
        self.surface.blit(self.background, (0, 0))    

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if worldviewport.rect.collidepoint(mouse_x, mouse_y) == True:
            game_world_x, game_world_y = worldviewport.screenpoint_to_gamepoint(mouse_x, mouse_y)
            text = "Mouse coords: (%d, %d)" % (game_world_x, game_world_y)
            font = self.font.render(text, True, (0, 0, 0))
            self.surface.blit(font, (0, 0))
