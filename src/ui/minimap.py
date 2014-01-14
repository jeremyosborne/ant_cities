import pygame
import ui.viewport as viewport
from assets.colors import entity_colors

class MiniMap(viewport.Viewport):
    def __init__(self, x=0, y=0, width=256, height=256, controller=None):
        """Arguments not inherited from viewport.
        
        controller {GameUIController} Provides a pipeline to events in the outside
        world.
        """
        
        viewport.Viewport.__init__(self, x, y, width, height)

        self.controller = controller

        # for initialization
        # Total size of our view taking into account the border.
        minimap_width = float(self.width)
        minimap_height = float(self.height)
        # Size of the game world.
        world_width = float(self.controller.world.width)
        world_height = float(self.controller.world.height)
        
        # Adjust for minimap aspect ratio, world size vs minimap size.
        # Determine the aspect ratio of the minimap.
        minimap_aspect_ratio = minimap_width/minimap_height
        # determine the aspect ratio of the world.
        world_aspect_ratio = world_width/world_height
        
        # Size the minimap to fit within our available aspect ratio.
        if (world_aspect_ratio >= 1) and (world_aspect_ratio >= minimap_aspect_ratio):
            # The dimensions of the minimap within the view.
            self.minimap_width = minimap_width
            self.minimap_height = world_height / (world_width / minimap_width)
            # Offset applied to the minimap within our available view.
            self.minimap_offsetx = 0
            self.minimap_offsety = (minimap_height - self.minimap_height) / 2
        else:
            self.minimap_width = world_width / (world_height / minimap_height)
            self.minimap_height = minimap_height
            # Calculate the offset of the minimap based on the aspect ratio.
            self.minimap_offsetx = (minimap_width - self.minimap_width) / 2
            self.minimap_offsety = 0

        if __debug__:
            print "MiniMap instance property values"
            print "minimap_width and height: ", self.minimap_width, self.minimap_height
            print "minimap_offset width and height: ", self.minimap_offsetx, self.minimap_offsety        

        # For scaling.
        self.x_scale_factor = float(self.minimap_width) / world_width
        self.y_scale_factor = float(self.minimap_height) / world_height 
        
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        self.minimap_surface = pygame.surface.Surface((self.minimap_width, self.minimap_height)).convert()
        self.minimap_surface.fill((0, 0, 0))
        
        # Panning of the map is active.
        self.panning_map = False

        # Register event listeners.
        controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        controller.sub("MOUSEBUTTONUP", self.mousebuttonup_listener)
        controller.sub("MOUSEMOTION", self.mousemotion_listener)

    def update(self):
        """Update the mini view of the game world.        
        """
        world = self.controller.game_simulation.world
        world_viewport = self.controller.game_simulation.world_viewport

        # Clear the mini map.
        self.minimap_surface.fill((0, 0, 0))
        # Let's go through all the entities and put them on the mini_map
        for entity in world.entities.itervalues():
            x_location, y_location = entity.location
            minimap_x = int(x_location * self.x_scale_factor)
            minimap_y = int(y_location * self.y_scale_factor)
            self.minimap_surface.fill(entity_colors(entity), (minimap_x, minimap_y, 2, 2))
            
        # Show visual area on the minimap.
        visible_rect = world_viewport.world_viewable_rect.copy()
        # Scale to fit.
        visible_rect.left = int(visible_rect.left * self.x_scale_factor)
        visible_rect.top = int(visible_rect.top * self.y_scale_factor)
        visible_rect.width = int(visible_rect.width * self.x_scale_factor)
        visible_rect.height = int(visible_rect.height * self.y_scale_factor)
        
        # Draw the layers of the minimap.
        pygame.draw.rect(self.minimap_surface, (255, 255, 0), visible_rect, 2)
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.minimap_surface, ((self.minimap_offsetx, self.minimap_offsety)))

    def mousebuttondown_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = True
    
    def mousemotion_listener(self, e):
        if self.panning_map == True:
            game_simulation = self.controller.game_simulation
            
            viewport_mouse_x, viewport_mouse_y = self.screenxy_to_relativexy(e.data["ev"].pos)
            
            # Define a rect that matches the actual area on the viewport 
            # where the minimap is, i.e. don't count the borders.
            minimap_rect = pygame.Rect(self.minimap_offsetx, self.minimap_offsety, self.minimap_width, self.minimap_height)

            if minimap_rect.collidepoint(viewport_mouse_x, viewport_mouse_y) == True:
                # Adjust mouse coordinates to match the viewport map.
                viewport_mouse_x = viewport_mouse_x - self.minimap_offsetx
                viewport_mouse_y = viewport_mouse_y - self.minimap_offsety
                                
                # Convert into gameworld coordinates.
                gameworld_x = int(viewport_mouse_x / self.x_scale_factor)
                gameworld_y = int(viewport_mouse_y / self.y_scale_factor)

                # Change centerpoint of the map.
                game_simulation.world_viewport.move_viewport(gameworld_x, gameworld_y)

    def mousebuttonup_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = False

