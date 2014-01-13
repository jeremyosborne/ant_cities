import pygame
import ui.viewport as viewport

class MouseDisplay(viewport.Viewport):
    """Display the mouse coordinates on the screen.
    """
    def __init__(self, x, y, controller):
        viewport.Viewport.__init__(self, x, y, 250, 20)

        self.font = pygame.font.SysFont("arial", 16)
        self.background = pygame.surface.Surface((250, 20)).convert()
        self.background.fill((255, 255, 255))
        # Make it such that when the surface is blitted on something else,
        # the background is transparent.
        self.surface.set_colorkey((255, 255, 255))
        
        self.controller = controller
        
    def update(self):
        
        world_viewport = self.controller.game_simulation.world_viewport

        # Clear the surface.
        self.surface.blit(self.background, (0, 0))    

        mouse_x, mouse_y = pygame.mouse.get_pos()
        game_world_x, game_world_y = world_viewport.screenpoint_to_gamepoint(mouse_x, mouse_y)
        text = "Mouse coords: (%d, %d)" % (game_world_x, game_world_y)
        font = self.font.render(text, True, (0, 0, 0))
        self.surface.blit(font, (0, 0))
