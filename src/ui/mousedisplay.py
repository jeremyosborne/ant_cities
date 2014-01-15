import pygame
from ui.pygameview import PygameView

class MouseDisplay(PygameView):
    """Display the translation of mouse device coordinates to mouse game world
    coordinates.
    """
    def subclass_init(self, **kwargs):
        self.font = pygame.font.SysFont("arial", 16)
        
        # Set transparency color.
        self.surface.set_colorkey((255, 255, 255))
    
    def clear(self):
        self.surface.fill((255, 255, 255))
    
    def draw(self, surface):
        game_world_x, game_world_y = self.controller.mouse_worldxy
        text = "Mouse coords: (%d, %d)" % (game_world_x, game_world_y)
        font = self.font.render(text, True, (0, 0, 0))
        self.surface.blit(font, (0, 0))
        
        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))

