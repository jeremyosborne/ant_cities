import pygame
from pymunk.vec2d import Vec2d
from common.ui.pygameview import PygameView

import ui.render.entity as render_entity

class Map(PygameView):
    def subclass_init(self, **kwargs):
        """Arguments not inherited from viewport.
        
        controller {GameUIController} Provides access to the outside world.
        """
        # Where do we switch to strategic view?
        self.strategic_zoom_level = len(self.controller.world_viewport.zoom_level_dims)-3
        
    def events_sub(self):
        self.subto(self.controller, "MOUSEBUTTONDOWN", self.mousebuttondown_listener)        
    
    def position(self):
        """Scale the map to the default size.
        """
        map_dims = self.controller.map_screen_dims()
        self.scale_relative_to_parent(map_dims["width_scale"], map_dims["height_scale"])
        self.position_relative_to_parent(map_dims["x"], map_dims["y"])
    
    def screenpoint_to_gamepoint(self, screenx, screeny):
        """Convert a screen coordinate to an equivalent game coordinate.
        
        screenx {number} Device X pixel location.
        screeny {number} Device Y pixel location.
        
        return {Vec2d} Converted (x, y) world location of the screen pixel.
        """
        world_viewport = self.controller.world_viewport
        # Determine scale factor.
        scale_factor_width = world_viewport.zoom_area_width/self.width
        scale_factor_height = world_viewport.zoom_area_height/self.height
        
        # Convert world coordinates to world viewable coordinates, then to viewport coordinates.
        return Vec2d(world_viewport.rect.centerx - world_viewport.zoom_area_width/2 + screenx*scale_factor_width,
                world_viewport.rect.centery - world_viewport.zoom_area_height/2 + screeny*scale_factor_height)

    def gamepoint_to_screenpoint(self, gamex, gamey):
        """Convert a game coordinate to an equivalent screen coordinate.
        
        gamex {number} Device X game world location.
        gamey {number} Device Y game world location.
        
        return {Vec2d} Converted (x, y) screen pixel corresponding to game world location.
        """
        world_viewport = self.controller.world_viewport
        x = (gamex - world_viewport.rect.left) / float(world_viewport.zoom_area_width) * self.width
        y = (gamey - world_viewport.rect.top) / float(world_viewport.zoom_area_height) * self.height
        
        return Vec2d(x, y)

    def scale_entity(self, surface):
        """Scale a surface according to the zoom level we are at.
        
        Always returns a surface, even if the surface wasn't scaled.
        """
        world_viewport = self.controller.world_viewport
        # Scale everything for now. Optimize later.
        w, h = surface.get_size()
        scale_width = int(w/(world_viewport.zoom_area_width/self.width))
        scale_height = int(h/(world_viewport.zoom_area_height/self.height))
        surface = pygame.transform.scale(surface, (scale_width, scale_height))
        return surface

    def render_entity(self, entity):
        """Display logic for dealing with entities.
        """
        zoom_level = self.controller.world_viewport.zoom_level
        # Render as scaled image or filled square? 
        if zoom_level > self.strategic_zoom_level:
            # Render as square.
            image = render_entity.strategic_icon(entity)
        else:
            image = self.controller.game_assets.image(entity)

            # This code is a bit less 'blech' now, and is generalized, but
            # it still needs to be refactored out of the Map.            
            image = render_entity.inventory(entity, image)
            if "facing" in entity.c:
                image = pygame.transform.rotate(image, entity.c["facing"].deg*-1.)
            image = render_entity.statusbars(entity, image)
            image = self.scale_entity(image)

        # Transform entity world coordinates to viewable coordinates.
        w, h = image.get_size()
        x, y = self.gamepoint_to_screenpoint(*entity.location)
        self.surface.blit(image, (x-w/2, y-h/2))

    def clear(self):
        self.surface.fill((255, 255, 255))
        
    def draw(self, surface):
        """Update the main view of the game world.
        """
        world = self.controller.world
        world_viewport = self.controller.world_viewport

        # Every round, publish an update of where the mouse is at relative to
        # the game world.
        self.controller.mouse_worldxy = self.screenpoint_to_gamepoint(*self.controller.mouse_screenxy)

        # If we are tracking an entity...
        if self.controller.entity_selection_track == True and self.controller.entity_selection:
            # ...move the view.
            self.controller.world_viewport.move(*self.controller.entity_selection.location)

        # Using the spatial index to determine what to render,
        # except let's not use the index if we're completely zoomed out. 
        if world_viewport.zoom_area_width != world.width:
            # Calculate the range.
            if world_viewport.zoom_area_width > world_viewport.zoom_area_height:
                the_range = world_viewport.zoom_area_width/2
            else:
                the_range = world_viewport.zoom_area_height/2
            
            entity_list_in_range = world.find_all_in_range(world_viewport.rect.center, the_range)
    
            # Render each entity onto the framebuffer.
            # Ignore the range.
            for entity, _ in entity_list_in_range:
                self.render_entity(entity)
        else:
            for entity in world.entities.itervalues():
                self.render_entity(entity)
    
        # If an entity is selected...
        ent = self.controller.entity_selection
        if ent and "destination" in ent.c:
            # ... and the entity has a destination, draw a line to the destination.
            dest_loc = ent.c["destination"].location
            if dest_loc:
                entx, enty = self.gamepoint_to_screenpoint(*ent.location)
                ent_loc = (int(entx), int(enty))
                destx, desty = self.gamepoint_to_screenpoint(*dest_loc)
                dest_loc = (int(destx), int(desty))
                color = (0, 150, 150)
                pygame.draw.line(self.surface, color, ent_loc, dest_loc)
                pygame.draw.circle(self.surface, color, ent_loc, 5)
                pygame.draw.circle(self.surface, color, dest_loc, 5)

        # Blit to the main surface.
        surface.blit(self.surface, (self.x, self.y))

    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        world = self.controller.world
        world_viewport = self.controller.world_viewport

        # For determining if we are inside the ui.
        ui_click_point = self.screenxy_to_relativexy(event.pos)
        
        if event.button == 1:
            # left click, attempt to select entity.
            
            # Clicks outside of the view won't cancel the tracking.
            if self.contained_screenxy(ui_click_point):
                game_world_point = self.screenpoint_to_gamepoint(*event.pos)
                entity, _ = world.find_closest(game_world_point, 150)
                self.controller.entity_selection = entity
        
        elif event.button == 4:  
            # Mouse Scroll Wheel Up == zoom in
            world_viewport.zoom_level += -1
            
            # Check to see if the mouse is above the game world viewport.
            if self.contained_screenxy(ui_click_point):
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                world_viewport.move(*gamexy)

        elif event.button == 5:  
            # Mouse Scroll Wheel Down == zoom out
            world_viewport.zoom_level += 1

            # Check to see if the mouse is above the game world viewport.
            if self.contained_screenxy(ui_click_point):
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                world_viewport.move(*gamexy)
