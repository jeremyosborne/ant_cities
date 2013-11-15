import viewport
import pygame

class Base_Panel(viewport.Viewport):
    
    def __init__(self, base, x_right=0, y_down=0, width=256, height=256):
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 1, True)
        self.base = base
        self.font = pygame.font.SysFont("arial", 16)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        
        #Add title to the background image.
        label = self.font.render("Base" + " " + self.base.description, True, (255, 255, 255))
        w, h = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        self.background.blit(self.font.render("Ant Count: ", True, (255, 255, 255)), (10, 15))
        self.background.blit(self.font.render("Energy: ", True, (255, 255, 255)), (10, 30))
        self.background.blit(self.font.render("Died: ", True, (255, 255, 255)), (10, 45))
        self.background.blit(self.font.render("Born: ", True, (255, 255, 255)), (10, 60))
        self.background.blit(self.font.render("Leaves Re: ", True, (255, 255, 255)), (10, 75))
        
        pygame.draw.line(self.background, (255, 255, 255), (self.width, 0), (self.width, self.height), 20)
        
        self.surface.blit(self.background, (0, 0))

        self.description = "Base " + self.base.description

    def update(self):

        self.surface.blit(self.background, (0, 0))
        self.surface.blit(self.font.render(str(self.base.ant_count), True, (255, 255, 255)), (90, 15))
        self.surface.blit(self.font.render(str(self.base.energy_units), True, (255, 255, 255)), (90, 30))
        self.surface.blit(self.font.render(str(self.base.ant_dead), True, (255, 255, 255)), (90, 45))
        self.surface.blit(self.font.render(str(self.base.ant_born), True, (255, 255, 255)), (90, 60))
        self.surface.blit(self.font.render(str(self.base.leaves_returned), True, (255, 255, 255)), (90, 75))

        

