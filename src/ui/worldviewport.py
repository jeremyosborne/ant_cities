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
        
        self.world_height = world_height
        self.world_width = world_width
        
        #A dictionary the holds information about our zoom level ranges.
        #zoom_level_ranges[1][0] = zoom level 1 width
        #zoom_level_ranges[1][1] = zoom level 1 height
        # ... to last zoom level
        #zoom_level_ranges['number of zoom levels'] = total number of zoom levels.  (integer)
        self.zoom_level_ranges = {}
        
        #Default zoom level - everything actual size.
        self.current_zoom_level = 2
    
        self.setup_viewable_area()
        
        #Scroll speed in pixels when moving in the lowest zoom level.
        self.scroll_speed_init = 10 / 1.5
        #Default number of pixels scrolled at a time. This value will be manipulated when the zoom
        #level changes.  Look in the update_zoom_level method.
        self.scroll_speed = self.scroll_speed_init * 1.5
        
        #Used if we want to put text directly on this viewport.
        self.font = pygame.font.SysFont("arial", 16)
        self.small_font = pygame.font.SysFont("arial", 13)

        # Register event listeners.
        if controller is not None:
            controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        elif __debug__:
            print "WARNING: controller was not defined, no event listening will be happening in", self

    #Setup    
    def setup_viewable_area(self):
        
        #Calculate the zoom levels.
        self.calculate_zoom_level_ranges()
        print "Printing zoom level ranges"
        print self.zoom_level_ranges
        
        #Setup variables for calculating the rectangle of the world that will be respresented in the viewport.
        self.zoom_area_width = self.zoom_level_ranges[self.current_zoom_level][0]
        self.zoom_area_height = self.zoom_level_ranges[self.current_zoom_level][1]

        #Define the area being represented in the viewport.  We start in the center of the world.
        self.world_viewable_center_x = self.world_width / 2
        self.world_viewable_center_min_x = self.zoom_area_width/2
        self.world_viewable_center_max_x = self.world_width - self.zoom_area_width/2
        self.world_viewable_center_y = self.world_height / 2
        self.world_viewable_center_min_y = self.zoom_area_height/2
        self.world_viewable_center_max_y = self.world_height - self.zoom_area_height/2
             
        self.world_viewable_x_rect = self.world_viewable_center_x - self.zoom_area_width/2
        self.world_viewable_y_rect = self.world_viewable_center_y - self.zoom_area_height/2
        self.world_viewable_rect = pygame.Rect(self.world_viewable_x_rect, self.world_viewable_y_rect, self.zoom_area_width, self.zoom_area_height)
      
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        print "background: ", self.width, self.height
        self.background.fill((255, 255, 255))
                             
    def calculate_zoom_level_ranges(self):
        #Zoom levels get bigger by a factor of 1.5.
        #Most zoomed in level available.  We're starting at index 1.
        self.zoom_level_ranges[1] =  (self.width / 1.5, self.height / 1.5)
        #Default zoom level no scaling.
        self.zoom_level_ranges[2] =  (self.width, self.height)
        
        #Calculate the remaining levels.
        finished_processing = True
        index = 2
        while finished_processing:
            index += 1
            #Test width and height of the next zoom level, is the next range still smaller than the world?
            if ((self.zoom_level_ranges[index - 1][0] * 1.5) <= self.world_width) and ((self.zoom_level_ranges[index -1][1] * 1.5) <= self.world_height):
                #Create the next zoom level entry.
                print "Creating next zoom level ", index
                self.zoom_level_ranges[index] = (self.zoom_level_ranges[index - 1][0] * 1.5, self.zoom_level_ranges[index - 1][1] * 1.5)
            else:
            #We're at the end of the line, so clean it up and end it.
                finished_processing = False
                #Check to see if we are already at the end of the line.  
                if self.zoom_level_ranges[index - 1][0] == self.width and self.zoom_level_ranges[index - 1][1] == self.world_height:
                    #We are at the end of the line and the last calculated zoom level is the highest.
                    self.zoom_level_ranges['number_of_zoom_levels'] = index - 1
                else:
                    self.zoom_level_ranges[index] = (self.world_width, self.world_height)
                    self.zoom_level_ranges['number_of_zoom_levels'] = index
                        
            
    @viewport.Viewport.width.setter
    def width(self, value):
        self.width = value
        self.setup_viewable_area()
        
    @viewport.Viewport.height.setter
    def height(self, value):
        self._height = value
        self.setup_viewable_area()

    def prepare_new_frame(self):
        self.surface.blit(self.background, (0, 0))        
    
    def render_entity(self, image, x, y, entity):
        
        w, h = image.get_size()
        
        #Are we in view?
        if self.world_viewable_rect.colliderect(pygame.Rect(x-w/2, y-h/2, w, h)):
            
            #Determine scale factor.  Used in calculating position in the viewport.
            scale_factor_width = self.zoom_area_width/self.width
            scale_factor_height = self.zoom_area_height/self.height
            
            #Convert object's coordinates to the viewport we're drawing on.
            #Convert world coordinates to world viewable coordinates, then to viewport coordinates.
            x = (x - (self.world_viewable_center_x - self.zoom_area_width/2)) / scale_factor_width 
            y = (y - (self.world_viewable_center_y - self.zoom_area_height/2)) / scale_factor_height
            
            #Render as scaled image or filled square? 
            if self.current_zoom_level > 5:
                #Render as square
                self.surface.fill(entity.color, (x-5, y-5, 10, 10))           
            else:
                #Render as scaled object
                if self.current_zoom_level != 2:  #Meaning scaling is required:
                    #scale the image
                    image = pygame.transform.scale(image, (int(w/scale_factor_width), int(h/scale_factor_height)))
                    w, h = image.get_size()
                self.surface.blit(image, (x-w/2, y-h/2))
                
            #print the mouse coordinates to the screen.  Being used for debugging purposes.  It's not the right place
            #for it anyway.
            #mouse_x, mouse_y = pygame.mouse.get_pos()
            #if self.rect.collidepoint(mouse_x, mouse_y) == True:
            #    game_world_x, game_world_y = self.screenpoint_to_gamepoint(mouse_x, mouse_y)
            #    text = self.font.render(str(game_world_x) + ", " + str(game_world_y), True, (0, 0, 0))
            #    w, h = text.get_size()
            #    self.surface.blit(text, (10, 90))

            
    #This will be for special rendering, such as effects that no matter what zoom level you're at, you want to see.
    #The following code needs to be modified to work with the new zoom rendering style.                 
    def force_render_entity(self, image, x, y):
        
        w, h = image.get_size()
        
        if self.viewport_rect.colliderect(pygame.Rect(x-w/2, y-h/2, w, h)):
            #We're in view.
            #Convert object's coordinates to the surface we're drawing on.
            x = x - (self.viewport_center_x - self.zoom_area_width/2)
            y = y - (self.viewport_center_y - self.zoom_area_height/2)
            self.zoom_frame_buffer.blit(image, (x-w/2, y-h/2)) 

    def update_viewport_center(self, x, y):
        """This method is called whenever one moves the map, i.e. changing the center of the viewport.
            It does all the necessary checks and corrects bad values passed in."""
        
        self.world_viewable_center_x = x
        self.world_viewable_center_y = y

        #Test to see if viewport center is out of range after the the zoom, if so, fix'um up.  This can happen if you're at the edge of the screen and then zoom out - the center will be close to the edge.        
        if self.world_viewable_center_x > self.world_viewable_center_max_x:
            self.world_viewable_center_x = self.world_viewable_center_max_x
        elif self.world_viewable_center_x < self.world_viewable_center_min_x:
            self.world_viewable_center_x = self.world_viewable_center_min_x
        if self.world_viewable_center_y > self.world_viewable_center_max_y:
            self.world_viewable_center_y = self.world_viewable_center_max_y
        elif self.world_viewable_center_y < self.world_viewable_center_min_y:
            self.world_viewable_center_y = self.world_viewable_center_min_y 
            
        self.world_viewable_x_rect = self.world_viewable_center_x - self.zoom_area_width/2
        self.world_viewable_y_rect = self.world_viewable_center_y - self.zoom_area_height/2
        self.world_viewable_rect = pygame.Rect(self.world_viewable_x_rect, self.world_viewable_y_rect, self.zoom_area_width, self.zoom_area_height)
            
    #When the zoom level is changed, several variables must be changed with it.
    def update_zoom_level(self, level):

        #Since I want the zoom to re-center based on mouse location in the gameworld, we need to calculate
        #that before we change any values below.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Check to see if the mouse is above the game world viewport any only make adjustments if so.
        #Will need to do something else for if the mouse is over the minimap.
        if self.rect.collidepoint(mouse_x, mouse_y) == True:
            game_world_x, game_world_y = self.screenpoint_to_gamepoint(mouse_x, mouse_y)
        else:
            game_world_x = self.world_viewable_center_x
            game_world_y = self.world_viewable_center_y
                        
        x, y = level
    
        self.zoom_area_width = x
        self.zoom_area_height = y
    
        self.world_viewable_center_min_x = self.zoom_area_width/2
        self.world_viewable_center_max_x = self.world_width - self.zoom_area_width/2

        self.world_viewable_center_min_y = self.zoom_area_height/2
        self.world_viewable_center_max_y = self.world_height - self.zoom_area_height/2

        self.update_viewport_center(game_world_x, game_world_y)

        #Change the scroll_speed based on the zoom level.
        self.scroll_speed = int (self.scroll_speed_init * 1.5 * self.current_zoom_level)
        
        if self.rect.collidepoint(mouse_x, mouse_y) == True:
            pygame.mouse.set_pos(self.gamepoint_to_screenpoint(game_world_x, game_world_y))

        #self.print_debug()
        
    def change_zoom_level(self, direction):
    
        if direction == "in":
            if self.current_zoom_level > 1:
                self.current_zoom_level -= 1
                self.update_zoom_level(self.zoom_level_ranges[self.current_zoom_level])
        if direction == "out":
            if self.current_zoom_level < self.zoom_level_ranges['number_of_zoom_levels']:
                self.current_zoom_level += 1
                self.update_zoom_level(self.zoom_level_ranges[self.current_zoom_level])

    def print_debug(self):
        print "world viewable rectangle:", self.world_viewable_rect
        print "zoom area width and height: ", self.zoom_area_width, self.zoom_area_height

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
        return Vec2d(self.world_viewable_center_x - self.zoom_area_width/2 + screenx*scale_factor_width,
                self.world_viewable_center_y - self.zoom_area_height/2 + screeny*scale_factor_height)

    def gamepoint_to_screenpoint(self, gamex, gamey):
        """Convert a game coordinate to an equivalent screen coordinate.
        
        gamex {number} Device X game world location.
        gamey {number} Device Y game world location.
        
        return {Vec2d} Converted (x, y) screen pixel corresponding to game world location.
        
        """
        
        x = (gamex - self.world_viewable_x_rect) / self.zoom_area_width * self.width
        y = (gamey - self.world_viewable_y_rect) / self.zoom_area_height * self.height
        
        return Vec2d(x, y)

    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        game_simulation = e.data["game_sim"]
        if event.button == 1:
            # left click, attempt to select entity.
            game_world_point = self.screenpoint_to_gamepoint(*event.pos)
            entity = game_simulation.world.spatial_index.find_closest(game_world_point, 150)[0]
            game_simulation.unit_information_display.set_unit(entity)
        elif event.button == 4:  
            # Mouse Scroll Wheel Up, so zoom in
            game_simulation.world.viewport.change_zoom_level("in")
        elif event.button == 5:  
            # Mouse Scroll Wheel Down, so zoom out
            game_simulation.world.viewport.change_zoom_level("out")
