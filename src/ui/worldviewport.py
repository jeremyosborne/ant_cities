import pygame
from pymunk.vec2d import Vec2d
import viewport

#This is our main game viewport.  It has a lot of custom code for this particular type of game, i.e. zooming and panning in a game world.
#So it doesn't belong in the main viewport class.
class WorldViewport(viewport.Viewport):
    def __init__(self, world_width, world_height, viewable_width, 
                 viewable_height, controller=None):
        """Arguments not inherited from viewport.
        
        controller {EventPublisher} Provides a pipeline to events in the outside
        world.
        """
        
        viewport.Viewport.__init__(self, 0, 0, viewable_width, viewable_height, 1, 0, True)
        
        self.description = "Game World Viewport"
        
        # Size of the game world.
        self.world_height = world_height
        self.world_width = world_width

        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((255, 255, 255))

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
        
        # Call once to initialize the first view.
        self.move_viewport()
        
        # Register event listeners.
        if controller is not None:
            controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        elif __debug__:
            print "WARNING: controller was not defined, no event listening will be happening in", self

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

    @property
    def world_viewable_center_max_x(self):
        """Maximum value allowed for center point x at this level.
        """
        return self.world_width - self.zoom_area_width/2

    @property
    def world_viewable_center_max_y(self):
        """Maximum value allowed for center point y at this zoom level.
        """
        return self.world_height - self.zoom_area_height/2

    @property
    def world_viewable_center_min_x(self):
        """Minimum value allowed for center point y at this zoom level.
        """
        return self.zoom_area_width/2

    @property
    def world_viewable_center_min_y(self): 
        """Minimum value allowed for center point y at this zoom level.
        """
        return self.zoom_area_height/2


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
            if ((next_zoom_level[0] <= self.world_width) and (next_zoom_level[1] <= self.world_height)):
                self.zoom_level_ranges.append(next_zoom_level)
            else:
                # Final zoom level. Make it match the size of the game world
                # even if it's not full factor zoom.
                self.zoom_level_ranges.append((self.world_width, self.world_height))
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
        
        x = x if x != None else self.world_width/2
        y = y if y != None else self.world_height/2

        # Test to see if viewport center is out of range after the the zoom, 
        # if so, fix'um up.  This can happen if you're at the edge of the 
        # screen and then zoom out - the center will be close to the edge.
        if x > self.world_viewable_center_max_x:
            x = self.world_viewable_center_max_x
        elif x < self.world_viewable_center_min_x:
            x = self.world_viewable_center_min_x
        if y > self.world_viewable_center_max_y:
            y = self.world_viewable_center_max_y
        elif y < self.world_viewable_center_min_y:
            y = self.world_viewable_center_min_y 

        # Update the visible area.
        self.world_viewable_rect.left = x - self.zoom_area_width/2
        self.world_viewable_rect.top = y - self.zoom_area_height/2
        self.world_viewable_rect.width = self.zoom_area_width
        self.world_viewable_rect.height = self.zoom_area_height

    def change_zoom_level(self, direction):
        new_zoom_level = self.current_zoom_level + direction
        # Boundary check.
        if new_zoom_level >= 0 and new_zoom_level < len(self.zoom_level_ranges):
            self.current_zoom_level = new_zoom_level
            
            # Re-center based on mouse location in the game world.
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check to see if the mouse is above the game world viewport.
            # Will need to do something else for if the mouse is over the minimap.
            if self.rect.collidepoint(mouse_x, mouse_y) == True:
                game_world_x, game_world_y = self.screenpoint_to_gamepoint(mouse_x, mouse_y)
            else:
                game_world_x = self.world_viewable_rect.centerx
                game_world_y = self.world_viewable_rect.centery
                
            self.move_viewport(game_world_x, game_world_y)
            
            if __debug__:
                print "Change of zoom level requested"
                print "zoom level == %s (requested change == %s)" % (self.current_zoom_level, direction)
                print "zoom area width and height: ", self.zoom_area_width, self.zoom_area_height
                print "world viewable rectangle:", self.world_viewable_rect

        # Buggy. When zooming out near edge scrolls mouse outside of view.
        #if self.rect.collidepoint(mouse_x, mouse_y) == True:
            # Move the mouse to the center of the zoom.
            #pygame.mouse.set_pos(self.gamepoint_to_screenpoint(game_world_x, game_world_y))

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
        
        x = (gamex - self.world_viewable_x_rect) / self.zoom_area_width * self.width
        y = (gamey - self.world_viewable_y_rect) / self.zoom_area_height * self.height
        
        return Vec2d(x, y)

    def update(self, world, draw=True):
        """Update the view of the game world.
        
        world {World} Gameworld reference.
        [draw] {bool} Override to allow temporary non-drawing of minimap.
        """

        if not draw:
            return

        # Clear.
        self.surface.blit(self.background, (0, 0))

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

        # Using the spatial index to determine what to render,
        # except let's not use the index if we're completely zoomed out. 
        if self.zoom_area_width != world.width:
            #Calculate the range.
            if self.zoom_area_width > self.zoom_area_height:
                the_range = self.zoom_area_width/2
            else:
                the_range = self.zoom_area_height/2
            
            entity_list_in_range = world.spatial_index.find_all_in_range((self.world_viewable_rect.centerx, self.world_viewable_rect.centery), the_range)
    
            #Render each entity onto the framebuffer.
            for entity in entity_list_in_range:
                self.render_entity(entity[0])
        else:
            for entity in world.entities.itervalues():
                self.render_entity(entity)

    def render_entity(self, entity):
        """Display logic for dealing with entities.
        """
        image = entity.image
        x, y = entity.location
        w, h = image.get_size()

        resource_bar_width = 25
        resource_bar_height = 4
        # colors
        resource_bar_empty = (255, 0, 0)
        resource_bar_full = (0, 255, 0)
        resource_bar = pygame.surface.Surface((resource_bar_width, resource_bar_height)).convert()

        #Are we in view?
        if self.world_viewable_rect.colliderect(pygame.Rect(x-w/2, y-h/2, w, h)):
            
            # Determine scale factor.  Used in calculating position in the viewport.
            scale_factor_width = self.zoom_area_width/self.width
            scale_factor_height = self.zoom_area_height/self.height
            
            # Convert object's coordinates to the viewport we're drawing on.
            # Convert world coordinates to world viewable coordinates, then to viewport coordinates.
            x = (x - (self.world_viewable_rect.centerx - self.zoom_area_width/2)) / scale_factor_width 
            y = (y - (self.world_viewable_rect.centery - self.zoom_area_height/2)) / scale_factor_height
            
            # Render as scaled image or filled square? 
            if self.current_zoom_level > self.strategic_zoom_level:
                # Render as square.
                self.surface.fill(entity.color, (x-5, y-5, 10, 10))           
            else:
                # Deal with ants. (Blech, this is gross right now, but trying
                # to isolate view code, view specific logic, and will then
                # normalize so that we simply do things to objects and need
                # no or fiew entity speicfic code paths).
                if entity.name == "ant":
                    image = pygame.transform.rotate(entity.image, entity.direction*-1.)
                    # Inventory display.
                    if self.current_zoom_level < self.strategic_zoom_level:
                        # If it's carrying a leaf, let's draw that too.
                        if entity.carry_image:
                            image = pygame.transform.rotate(entity.carry_image, entity.direction*-1.)
                            w, h = entity.image.get_size()
                    
                    # Energy/health bar display.
                    if self.current_zoom_level < self.strategic_zoom_level:
                        # Energy.
                        resource_bar.fill(resource_bar_empty)
                        resource_bar.fill(resource_bar_full, (0, 0, (entity.energy_current/entity.max_energy)*resource_bar_width, resource_bar_height))
                        image.blit(resource_bar, (0, 0))
                        # Health.
                        resource_bar.fill(resource_bar_empty)
                        resource_bar.fill(resource_bar_full, (0, 0, (entity.health_current/entity.max_health)*resource_bar_width, resource_bar_height))
                        image.blit(resource_bar, (0, resource_bar_height+1))
                        

                # Scaling according to zoom level.
                if self.current_zoom_level != 1:
                    image = pygame.transform.scale(image, (int(w/scale_factor_width), int(h/scale_factor_height)))
                    w, h = image.get_size()
                self.surface.blit(image, (x-w/2, y-h/2))

    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        game_simulation = e.data["game_sim"]
        
        if event.button == 1:
            # left click, attempt to select entity.
            
            # Determine if we clicked within the viewable UI.
            ui_click_point = self.screenxy_to_relativexy(event.pos)
            ui_container = pygame.Rect(0, 0, self.width, self.height)

            # Clicks outside of the view won't cancel the tracking.
            if ui_container.collidepoint(ui_click_point) == True:
                game_world_point = self.screenpoint_to_gamepoint(*event.pos)
                entity = game_simulation.world.spatial_index.find_closest(game_world_point, 150)[0]
                game_simulation.unit_information_display.set_unit(entity)
        
        if event.button == 4:  
            # Mouse Scroll Wheel Up == zoom in
            self.change_zoom_level(-1)
        elif event.button == 5:  
            # Mouse Scroll Wheel Down == zoom out
            self.change_zoom_level(1)
