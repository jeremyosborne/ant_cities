import pygame
from pymunk.vec2d import Vec2d
from ui.pygameview import PygameView
from ui.assets.colors import entity_colors
from ui.assets.images import entity_images

class Map(PygameView):
    def subclass_init(self, **kwargs):
        """Arguments not inherited from viewport.
        
        controller {GameUIController} Provides access to the outside world.
        """
        # Number of pixel buffer from the edges of our view within we scroll.
        self.scroll_buffer = 20
        # How many visual pixels do we move per frame when scrolling?
        self.scroll_speed_multiplier = 20
        
        # Where do we switch to strategic view?
        self.strategic_zoom_level = len(self.controller.world_viewport.zoom_level_dims)-3
        
        # Register event listeners.
        # TODO: Need a way to unsubscribe listeners.
        self.controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        
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

    def render_entity_statusbars(self, entity, surface):
        """Display status bars for a particular entity.
        
        Pass the entity and the surface on which to render the status bars.
        
        Returns the surface with the status bars rendered.
        """
        # Common settings.
        width = 25
        height = 4
        empty_color = (255, 0, 0)
        bar = pygame.surface.Surface((width, height)).convert()
        
        # Energy.
        comps_to_draw = [(entity.c["energy"], (230, 100, 230)),
                         (entity.c["health"], (0, 255, 0))]
        for i, v in enumerate(comps_to_draw):
            component, full_color = v
            bar.fill(empty_color)
            bar.fill(full_color, (0, 0, component.val/float(component.max)*width, height))
            surface.blit(bar, (0, height*i))
        return surface

    def render_scaling(self, surface):
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

    def render_entity_strategic_icon(self, entity):
        """Renders the entity as a strategic icon on the view surface.
        """
        color = entity_colors(entity)
        # Transform entity world coordinates to viewable coordinates.
        x, y = self.gamepoint_to_screenpoint(*entity.location)
        self.surface.fill(color, (x-5, y-5, 10, 10))
    
    def render_entity(self, entity):
        """Display logic for dealing with entities.
        """
        zoom_level = self.controller.world_viewport.zoom_level
        # Render as scaled image or filled square? 
        if zoom_level > self.strategic_zoom_level:
            # Render as square.
            self.render_entity_strategic_icon(entity)
        else:
            image = entity_images(entity)
            
            # Do special things to the dummy.
#             if __debug__:
#                 if entity.name == "dummy":
#                     image = pygame.transform.rotate(image, entity.c["facing"].deg*-1.)
            
            # Deal with ants. (Blech, this is gross right now, but trying
            # to isolate view code, view specific logic, and will then
            # normalize so that we simply do things to objects and need
            # no or few entity specific code paths).            
            if entity.name == "ant":
                image = pygame.transform.rotate(image, entity.c["facing"].deg*-1.)
                # Inventory display.
                if zoom_level < self.strategic_zoom_level:
                    if entity.c["inventory"].carried:
                        # We assume ants are only carrying a leaf.
                        inventory_image = entity_images(entity.c["inventory"].carried[0])
                        image = pygame.transform.rotate(inventory_image, entity.c["facing"].deg*-1.)

                if zoom_level < self.strategic_zoom_level:
                    # Energy/health bar display.
                    image = self.render_entity_statusbars(entity, image)

            image = self.render_scaling(image)

            w, h = image.get_size()
            # Transform entity world coordinates to viewable coordinates.
            x, y = self.gamepoint_to_screenpoint(*entity.location)
            self.surface.blit(image, (x-w/2, y-h/2))

    def clear(self):
        self.surface.fill((255, 255, 255))
        
    def draw(self, surface):
        """Update the main view of the game world.
        """
        world = self.controller.world
        world_viewport = self.controller.world_viewport

        # Pan if mouse near border of game.
        # Scroll speed of view (in pixels)
        scroll_speed = (world_viewport.zoom_level+1)*world_viewport.zoom_factor*self.scroll_speed_multiplier

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 0 and mouse_x <= self.scroll_buffer:
            world_viewport.scroll(x=-scroll_speed)
        elif (mouse_x >= self.width-self.scroll_buffer) and mouse_x <= self.width:
            world_viewport.scroll(x=scroll_speed)
        if mouse_y >= 0 and mouse_y <= self.scroll_buffer:
            world_viewport.scroll(y=-scroll_speed)
        elif (mouse_y >= self.height-self.scroll_buffer) and mouse_y <= self.height:
            world_viewport.scroll(y=scroll_speed)

        # Every round, publish an update of where the mouse is at relative to
        # the game world.
        self.controller.mouse_worldxy = self.screenpoint_to_gamepoint(mouse_x, mouse_y)

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
            for entity in entity_list_in_range:
                self.render_entity(entity[0])
        else:
            for entity in world.entities.itervalues():
                self.render_entity(entity)
    
        # If an entity is selected...
        if self.controller.entity_selection:
            # ... and the entity has a destination, draw a line to the destination.
            ent = self.controller.entity_selection
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
        surface.blit(self.surface, ((self.x, self.y)))

    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        world = self.controller.world
        world_viewport = self.controller.world_viewport

        # For determining if we are inside the ui.
        ui_click_point = self.screenxy_to_relativexy(event.pos)
        
        if event.button == 1:
            # left click, attempt to select entity.
            
            # Clicks outside of the view won't cancel the tracking.
            if self.rect.collidepoint(ui_click_point) == True:
                game_world_point = self.screenpoint_to_gamepoint(*event.pos)
                entity, _ = world.find_closest(game_world_point, 150)
                self.controller.entity_selection = entity
        
        elif event.button == 4:  
            # Mouse Scroll Wheel Up == zoom in
            world_viewport.zoom_level += -1
            
            # Check to see if the mouse is above the game world viewport.
            if self.rect.collidepoint(ui_click_point) == True:
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                world_viewport.move(*gamexy)

        elif event.button == 5:  
            # Mouse Scroll Wheel Down == zoom out
            world_viewport.zoom_level += 1

            # Check to see if the mouse is above the game world viewport.
            if self.rect.collidepoint(ui_click_point) == True:
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                world_viewport.move(*gamexy)
