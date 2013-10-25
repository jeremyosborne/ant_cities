import pygame
import viewport

class FPS_Display(viewport.Viewport):
    def __init__(self):
        viewport.Viewport.__init__(self, 5, 5, 125, 20, 1, 10, True)
        self.font = pygame.font.SysFont("arial", 16)
        self.background = pygame.surface.Surface((125, 20)).convert()
        self.background.fill((255, 255, 255))
        #Make it such that when the surface is blitted on something else,
        #the background is transparent.
        self.surface.set_colorkey((255, 255, 255))
        self.description = "FPS display."
        
    def draw_fps(self, clock):
        fps = clock.get_fps()

        #Clear the surface.
        self.surface.blit(self.background, (0, 0))    

        label = self.font.render(str(fps), True, (0, 0, 0))
        self.surface.blit(label, (0, 0))
        
    def service_user_event(self, event, game_simulation):
        pass
