"""NOT IMPLEMENTED.
"""

import globaldata
from entities.gameentity import GameEntity

class Spider(GameEntity):
    
    def __init__(self, world, image):
        ##
        raise NotImplementedError("Spider has not been correctly implemented.")
        ##
        GameEntity.__init__(self, world, "spider", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.speed = 50. + randint(-20, 20)
        self.color = (128,128,128)
        
    def bitten(self):
        
        self.health -= 1
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image
        self.speed = 140.
        
    def render(self, surface):
        
        GameEntity.render(self, surface)
                
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill( (0, 255, 0), (bar_x, bar_y, self.health, 4))
        
    def process(self, time_passed):
        
        x, y = self.location
        if x > globaldata.WORLD_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        
        GameEntity.process(self, time_passed)
