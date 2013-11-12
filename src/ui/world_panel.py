import viewport
import time
import pygame

class World_Panel(viewport.Viewport):
    
    def __init__(self, world, x_right=0, y_down=0, width=256, height=256):
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 1, True)
        self.world = world
        self.font = pygame.font.SysFont("arial", 16)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        
        #Add title to the background image.
        label = self.font.render("World Info", True, (255, 255, 255))
        w, h = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        self.background.blit(self.font.render("Game Time (s): ", True, (255, 255, 255)), (10, 15))
        self.background.blit(self.font.render("Base Count: ", True, (255, 255, 255)), (10, 30))
        self.background.blit(self.font.render("Leaves Born: ", True, (255, 255, 255)), (10, 45))
        self.background.blit(self.font.render("Leaves Died: ", True, (255, 255, 255)), (10, 60))
        self.background.blit(self.font.render("Nothing: ", True, (255, 255, 255)), (10, 75))
        
        pygame.draw.line(self.background, (255, 255, 255), (self.width, 0), (self.width, self.height), 20)
        
        self.surface.blit(self.background, (0, 0))

        self.description = "World Info Panel"

    def update(self):

        self.surface.blit(self.background, (0, 0))
        self.surface.blit(self.font.render(str(int(time.time() - self.world.time_born)), True, (255, 255, 255)), (120, 15))
        self.surface.blit(self.font.render(str(self.world.base_count), True, (255, 255, 255)), (120, 30))
        self.surface.blit(self.font.render(str(self.world.leaf_count), True, (255, 255, 255)), (120, 45))
        self.surface.blit(self.font.render(str(self.world.leaf_expired), True, (255, 255, 255)), (120, 60))
        self.surface.blit(self.font.render(str("None"), True, (255, 255, 255)), (120, 75))

        

