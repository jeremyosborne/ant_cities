import pygame
from pymunk.vec2d import Vec2d
import ui.viewport as viewport
from ui.assets.colors import entity_colors
from ui.assets.images import entity_images
from commonmath import mmval

#This is our main game viewport.  It has a lot of custom code for this particular type of game, i.e. zooming and panning in a game world.
#So it doesn't belong in the main viewport class.
class WorldViewport(viewport.Viewport):
    def __init__(self, viewable_width, viewable_height, controller):
        """Arguments not inherited from viewport.
        
        controller {GameUIController} Provides access to the outside world.
        """
        
        viewport.Viewport.__init__(self, 0, 0, viewable_width, viewable_height)
        
        self.controller = controller
        
        # zoom-in/out factor per zoom level.
        self.zoom_factor = 1.5
        
        # Number of pixel buffer from the edges of our view within we scroll.
        self.scroll_buffer = 20
        # How many visual pixels do we move per frame when scrolling?
        self.scroll_speed_multiplier = 20

        # List of zoom level dimensions.
        # Index == the zoom level (lower == more zoomed in)
        # Dimensions are a tuple (width, height) of pixels viewable.
        self.zoom_level_ranges = []

        # Calculate the zoom levels.
        self.calculate_zoom_level_ranges()

        # Default zoom level (needs to be done after zoom level calculation).
        self.current_zoom_level = len(self.zoom_level_ranges)-1
        # Where do we switch to strategic view?
        self.strategic_zoom_level = len(self.zoom_level_ranges)-3
        
        # Defines the viewable portion of the entire world.
        # Initial values are set in the move_viewport call.
        self.world_viewable_rect = pygame.Rect(0, 0, 0, 0)
        
        # Initialize the first view.
        self.change_zoom_level(0)
        self.move_viewport()
        
        # Register event listeners.
        # TODO: Need a way to unsubscribe listeners.
        controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        
    @property
    def zoom_area_width(self):
        """Width in pixels at the current zoom level.
        """
        return self.zoom_level_ranges[self.current_zoom_level][0]

    @property
    def zoom_area_height(self):
        """Height in pixels at the current zoom level.
        """
        return self.zoom_level_ranges[self.current_zoom_level][1]
    
    @property
    def scroll_speed(self):
        """Scroll speed of view (in pixels).
        """
        return (self.current_zoom_level+1)*self.zoom_factor*self.scroll_speed_multiplier

    def calculate_zoom_level_ranges(self):
        """Populates the zoom_level_ranges list.
        
        Call once, and only once.
        """
        # Remove if and when we want this to be called more than once.
        assert len(self.zoom_level_ranges) == 0, "Function should be called only once."
        
        # Most zoomed in: allow one level of up-scaling.
        self.zoom_level_ranges.append((self.width/self.zoom_factor, self.height/self.zoom_factor))
        # Default zoom level no scaling.
        self.zoom_level_ranges.append((self.width, self.height))
        
        # Calculate the remaining levels.
        while True:
            # Keep building zoom levels until the max zoom level encompasses the
            # entire game world.
            current_zoom_level = self.zoom_level_ranges[-1]
            next_zoom_level = (current_zoom_level[0]*self.zoom_factor, 
                               current_zoom_level[1]*self.zoom_factor)
            if ((next_zoom_level[0] <= self.controller.world.width) and (next_zoom_level[1] <= self.controller.world.height)):
                self.zoom_level_ranges.append(next_zoom_level)
            else:
                # Final zoom level. Make it match the size of the game world
                # even if it's not full factor zoom.
                self.zoom_level_ranges.append((self.controller.world.width, self.controller.world.height))
                break

        if __debug__:
            print "Zoom level ranges (%s total zoom levels)" % len(self.zoom_level_ranges)
            print self.zoom_level_ranges
    
    def scroll_viewport(self, x=0, y=0):
        """Scrolls the viewport relative to its current position.
        
        (x, y) are offsets applied as a delta to the current position of the
        center.
        
        """
        # Convenience method, handoff to move_viewport.
        self.move_viewport(self.world_viewable_rect.centerx+x,
                           self.world_viewable_rect.centery+y)
    
    def move_viewport(self, x=None, y=None):
        """Moves the viewport and adjusts the dimensions of the bounding
        rectangle.
        
        (x, y) make up the new center coordinate for the viewport.
        
        Needs to be called to to after zoom level changes, too.
        """
        
        x = x if x != None else self.controller.world.width/2
        y = y if y != None else self.controller.world.height/2

        # Test to see if viewport center is out of range after the the zoom, 
        # if so, fix'um up.  This can happen if you're at the edge of the 
        # screen and then zoom out - the center will be close to the edge.
        x = mmval(self.controller.world.width - self.zoom_area_width/2, x, self.zoom_area_width/2)
        y = mmval(self.controller.world.height - self.zoom_area_height/2, y, self.zoom_area_height/2)

        # Update the visible area.
        self.world_viewable_rect.center = (x, y)

    def change_zoom_level(self, direction):
        """Changes the zoom level and resizes the viewable area.
        
        direction {number} Relative change. Passing 0 will not change the
        zoom level but will perform operations, like setting the size of
        the viewable rectangle.
        """
        new_zoom_level = self.current_zoom_level + direction
        # Boundary check.
        if new_zoom_level >= 0 and new_zoom_level < len(self.zoom_level_ranges):
            self.current_zoom_level = new_zoom_level

            # Resize the viewable area.
            self.world_viewable_rect.width = self.zoom_area_width
            self.world_viewable_rect.height = self.zoom_area_height
                        
            # Correct the center point.
            self.move_viewport(*self.world_viewable_rect.center)
            
#             if __debug__:
#                 print "Change of zoom level requested"
#                 print "zoom level == %s (requested change == %s)" % (self.current_zoom_level, direction)
#                 print "zoom area width and height: ", self.zoom_area_width, self.zoom_area_height
#                 print "world viewable rectangle:", self.world_viewable_rect

    def screenpoint_to_gamepoint(self, screenx, screeny):
        """Convert a screen coordinate to an equivalent game coordinate.
        
        screenx {number} Device X pixel location.
        screeny {number} Device Y pixel location.
        
        return {Vec2d} Converted (x, y) world location of the screen pixel.
        """
        # Determine scale factor.
        scale_factor_width = self.zoom_area_width/self.width
        scale_factor_height = self.zoom_area_height/self.height
        
        # Convert world coordinates to world viewable coordinates, then to viewport coordinates.
        return Vec2d(self.world_viewable_rect.centerx - self.zoom_area_width/2 + screenx*scale_factor_width,
                self.world_viewable_rect.centery - self.zoom_area_height/2 + screeny*scale_factor_height)

    def gamepoint_to_screenpoint(self, gamex, gamey):
        """Convert a game coordinate to an equivalent screen coordinate.
        
        gamex {number} Device X game world location.
        gamey {number} Device Y game world location.
        
        return {Vec2d} Converted (x, y) screen pixel corresponding to game world location.
        """
        
        x = (gamex - self.world_viewable_rect.left) / float(self.zoom_area_width) * self.width
        y = (gamey - self.world_viewable_rect.top) / float(self.zoom_area_height) * self.height
        
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
        if self.current_zoom_level != 1:
            w, h = surface.get_size()
            scale_width = int(w/(self.zoom_area_width/self.width))
            scale_height = int(h/(self.zoom_area_height/self.height))
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
        # Render as scaled image or filled square? 
        if self.current_zoom_level > self.strategic_zoom_level:
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
                if self.current_zoom_level < self.strategic_zoom_level:
                    if entity.c["inventory"].carried:
                        # We assume ants are only carrying a leaf.
                        inventory_image = entity_images(entity.c["inventory"].carried[0])
                        image = pygame.transform.rotate(inventory_image, entity.c["facing"].deg*-1.)

                if self.current_zoom_level < self.strategic_zoom_level:
                    # Energy/health bar display.
                    image = self.render_entity_statusbars(entity, image)

            image = self.render_scaling(image)

            w, h = image.get_size()
            # Transform entity world coordinates to viewable coordinates.
            x, y = self.gamepoint_to_screenpoint(*entity.location)
            self.surface.blit(image, (x-w/2, y-h/2))

    def update(self):
        """Update the main view of the game world.
        """
        world = self.controller.game_simulation.world
        
        # Clear.
        self.surface.fill((255, 255, 255))

        # Pan if mouse near border of game.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 0 and mouse_x <= self.scroll_buffer:
            self.scroll_viewport(x=-self.scroll_speed)
        elif (mouse_x >= self.width-self.scroll_buffer) and mouse_x <= self.width:
            self.scroll_viewport(x=self.scroll_speed)
        if mouse_y >= 0 and mouse_y <= self.scroll_buffer:
            self.scroll_viewport(y=-self.scroll_speed)
        elif (mouse_y >= self.height-self.scroll_buffer) and mouse_y <= self.height:
            self.scroll_viewport(y=self.scroll_speed)

        # Every round, publish an update of where the mouse is at relative to
        # the game world.
        self.controller.mouse_worldxy = self.screenpoint_to_gamepoint(mouse_x, mouse_y)

        # If we are tracking an entity...
        if self.controller.entity_selection_track == True and self.controller.entity_selection:
            # ...move the view.
            self.move_viewport(*self.controller.entity_selection.location)

        # Using the spatial index to determine what to render,
        # except let's not use the index if we're completely zoomed out. 
        if self.zoom_area_width != world.width:
            # Calculate the range.
            if self.zoom_area_width > self.zoom_area_height:
                the_range = self.zoom_area_width/2
            else:
                the_range = self.zoom_area_height/2
            
            entity_list_in_range = world.find_all_in_range(self.world_viewable_rect.center, the_range)
    
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
    
    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        game_simulation = self.controller.game_simulation

        # For determining if we are inside the ui.
        ui_click_point = self.screenxy_to_relativexy(event.pos)
        
        if event.button == 1:
            # left click, attempt to select entity.
            
            # Clicks outside of the view won't cancel the tracking.
            if self.rect.collidepoint(ui_click_point) == True:
                game_world_point = self.screenpoint_to_gamepoint(*event.pos)
                entity, _ = game_simulation.world.find_closest(game_world_point, 150)
                self.controller.entity_selection = entity
        
        elif event.button == 4:  
            # Mouse Scroll Wheel Up == zoom in
            self.change_zoom_level(-1)
            
            # Check to see if the mouse is above the game world viewport.
            if self.rect.collidepoint(ui_click_point) == True:
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                self.move_viewport(*gamexy)

        elif event.button == 5:  
            # Mouse Scroll Wheel Down == zoom out
            self.change_zoom_level(1)

            # Check to see if the mouse is above the game world viewport.
            if self.rect.collidepoint(ui_click_point) == True:
                gamexy = self.screenpoint_to_gamepoint(*event.pos)
                self.move_viewport(*gamexy)
