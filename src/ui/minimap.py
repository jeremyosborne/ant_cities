import pygame
from ui.pygameview import PygameView

class MiniMap(PygameView):
    def subclass_init(self, **kwargs):        
        # Panning of the map is active.
        self.panning_map = False

    def init_surface(self, width=None, height=None):
        """Override and allow redrawing of the minimap.
        """
        super(MiniMap, self).init_surface(width, height)
        self.minimap_surface = pygame.surface.Surface((self.minimap_width, self.minimap_height)).convert()

    @property
    def desired_aspect_ratio(self):
        """What is the desired aspect ratio?
        
        landscape > 1
        portrait < 1
        square == 0
        """
        # We base our desired aspect ratio on the real size of the world.
        # Name of the function is to allow growth into an aspect ratio mixin
        # without changing this code.
        return float(self.controller.world.width)/self.controller.world.height

    @property
    def minimap_width(self):
        """Width of the minimap (minus container and padding).
        """
        world_width = float(self.controller.world.width)
        world_height = float(self.controller.world.height)

        try:
            if self.desired_aspect_ratio >= 1:
                # Landscape
                return self.width  
            else:
                # Portrait
                return world_width / (world_height / float(self.height))
        except ZeroDivisionError:
            # In case height is 0.
            return 0
        
    @property
    def minimap_height(self):
        """Height of the minimap (minus container and padding).
        """
        world_width = float(self.controller.world.width)
        world_height = float(self.controller.world.height)

        try:
            if self.desired_aspect_ratio >= 1:
                # Landscape
                return world_height / (world_width / self.width)
            else:
                # Portrait
                return self.height
        except ZeroDivisionError:
            # In case width is 0.
            return 0

    @property
    def minimap_offsetx(self):
        """Left anchor for minimap.
        """
        if self.desired_aspect_ratio >= 1:
            # Landscape
            return 0
        else:
            # Portrait
            return (self.width - self.minimap_width) / 2

    @property
    def minimap_offsety(self):
        """Top anchor for minimap.
        """
        if self.desired_aspect_ratio >= 1:
            # Landscape
            return (self.height - self.minimap_height) / 2
        else:
            # Portrait
            return 0

    @property
    def x_scale_factor(self):
        """Used to scale normal objects down to the on screen size of the
        minimap.
        """
        return float(self.minimap_width) / self.controller.world.width

    @property
    def y_scale_factor(self):
        """Used to scale normal objects down to the on screen size of the
        minimap.
        """
        return float(self.minimap_height) / self.controller.world.height

    def events_sub(self):
        self.subto(self.controller, "MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        self.subto(self.controller, "MOUSEBUTTONUP", self.mousebuttonup_listener)
        self.subto(self.controller, "MOUSEMOTION", self.mousemotion_listener)

    def clear(self):
        self.surface.fill((0, 0, 0))
        # Also clear the minimap.
        self.minimap_surface.fill((0, 0, 0))

    def draw(self, surface):
        """Update the mini view of the game world.        
        """
        world = self.controller.game_engine.world

        # Let's go through all the entities and put them on the mini_map
        for entity in world.entities.itervalues():
            x_location, y_location = entity.location
            minimap_x = int(x_location * self.x_scale_factor)
            minimap_y = int(y_location * self.y_scale_factor)
            self.minimap_surface.fill(self.controller.game_assets.color(entity), (minimap_x, minimap_y, 2, 2))
            
        # Show visual area on the minimap.
        scaled_world_viewport = self.controller.world_viewport.rect.copy()
        # Scale to fit.
        scaled_world_viewport.left = int(scaled_world_viewport.left * self.x_scale_factor)
        scaled_world_viewport.top = int(scaled_world_viewport.top * self.y_scale_factor)
        scaled_world_viewport.width = int(scaled_world_viewport.width * self.x_scale_factor)
        scaled_world_viewport.height = int(scaled_world_viewport.height * self.y_scale_factor)
        
        # Draw the layers of the minimap.
        pygame.draw.rect(self.minimap_surface, (255, 255, 0), scaled_world_viewport, 2)
        self.surface.blit(self.minimap_surface, ((self.minimap_offsetx, self.minimap_offsety)))

        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))

    def mousebuttondown_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = True
    
    def mousemotion_listener(self, e):
        if self.panning_map == True:
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
                self.controller.world_viewport.move(gameworld_x, gameworld_y)

    def mousebuttonup_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = False

