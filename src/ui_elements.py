#Game specific UI element class definitions.
#Examples:  Mini-map.


import pygame
from pygame.locals import *

import viewport
import global_data


#This is our main game viewport.  It has a lot of custom code for this particular type of game, i.e. zooming and panning in a game world.
#So it doesn't belong in the main viewport class.

class World_Viewport(viewport.Viewport):
    def __init__(self, world_width, world_height):
        viewport.Viewport.__init__(self, 0, 0, global_data.screen_size_x, global_data.screen_size_y, 1, 0, True)

        self.zoom_area_width = global_data.screen_size_x
        self.zoom_area_height = global_data.screen_size_y
        self.world_height = world_height
        self.world_width = world_width
        
        #Hard coded Zoom level for testing
        #Zoom levels as tuples.
        self.zoom_level_1 = (global_data.screen_size_x/2, global_data.screen_size_y/2)
        self.zoom_level_2 = (global_data.screen_size_x, global_data.screen_size_y)
        self.zoom_level_3 = (global_data.screen_size_x+global_data.screen_size_x/2, global_data.screen_size_y+global_data.screen_size_y/2)
        self.zoom_level_4 = (global_data.screen_size_x*2, global_data.screen_size_y*2)
        self.zoom_level_5 = (global_data.screen_size_x*3, global_data.screen_size_y*3)
        self.zoom_level_6 = (self.world_width, self.world_height)
        #List of tuples representing the zoom levels
        self.zoom_levels = (self.zoom_level_1, self.zoom_level_2, self.zoom_level_3, self.zoom_level_4, self.zoom_level_5, self.zoom_level_6)

        #default zoom level
        self.zoom_level = 2

        #Scroll speeds that will be used based on zoom level
        self.scroll_speeds = (5, 10, 20, 40, 60, 100)
        #default scroll speed
        self.scroll_speed = 10

        self.viewport_center_x = self.world_width / 2
        self.viewport_center_min_x = self.zoom_area_width/2
        self.viewport_center_max_x = self.world_width - self.zoom_area_width/2
        self.viewport_center_y = self.world_height / 2
        self.viewport_center_min_y = self.zoom_area_height/2
        self.viewport_center_max_y = self.world_height - self.zoom_area_height/2

        #Defining the rectangle of the viewport
        self.viewport_x_rect = self.viewport_center_x - self.zoom_area_width/2
        self.viewport_y_rect = self.viewport_center_y - self.zoom_area_height/2
        self.viewport_rect = pygame.Rect(self.viewport_x_rect, self.viewport_y_rect, self.zoom_area_width, self.zoom_area_height)

        #The zoom_frame_buffer is the surface where everything is rendered (blited) to.  It will then be scaled to fit the viewport.
        self.zoom_frame_buffer = pygame.surface.Surface((self.zoom_area_width, self.zoom_area_height)).convert()
        
        #Let's prepare the backgound image.  It will just be white.
        self.background = pygame.surface.Surface((self.zoom_area_width, self.zoom_area_height)).convert()
        self.background.fill((255, 255, 255))

    def prepare_new_frame(self):
        self.zoom_frame_buffer.blit(self.background, (0, 0))

    #We check to see if it's in the field of vision and render if so.
    def render_entity(self, image, x, y):
        
        w, h = image.get_size()
        
        if self.viewport_rect.colliderect(pygame.Rect(x-w/2, y-h/2, w, h)):
            #We're in view.
            #Convert object's coordinates to the surface we're drawing on.
            x = x - (self.viewport_center_x - self.zoom_area_width/2)
            y = y - (self.viewport_center_y - self.zoom_area_height/2)
            self.zoom_frame_buffer.blit(image, (x-w/2, y-h/2))
    
    #Maybe sometime in the future
    def calculate_zoom_levels(self):
        pass

    def in_field_of_vision(self):
        pass

    #A function for updating the viewport center point.  Other variables are updated also to keep everything in sync.  Called only from the x, y adjustment functions found further below.
    #On the other hand, one could call this directly if one was implementing a feature to follow a moving unit.
    def update_viewport_center(self, x, y):
       
        self.viewport_center_x = x
        self.viewport_center_y = y
        self.viewport_x_rect = x - self.zoom_area_width/2
        self.viewport_y_rect = y - self.zoom_area_height/2
        self.viewport_rect = pygame.Rect(self.viewport_x_rect, self.viewport_y_rect, self.zoom_area_width, self.zoom_area_height)
    
    def add_to_viewport_x(self, what_to_add):
    
        #Go ahead and make the adjustment if we're not going over the max center point.
        if self.viewport_center_x + what_to_add < self.viewport_center_max_x:
            self.update_viewport_center(self.viewport_center_x + what_to_add, self.viewport_center_y) 
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.viewport_center_max_x, self.viewport_center_y)
        
    def subtract_from_viewport_x(self, what_to_subtract):
    
        #Go ahead and make the adjustment if we're not going under the min center point.
        if self.viewport_center_x - what_to_subtract > self.viewport_center_min_x:
            self.update_viewport_center(self.viewport_center_x - what_to_subtract, self.viewport_center_y)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.viewport_center_min_x, self.viewport_center_y)
             
    def add_to_viewport_y(self, what_to_add):
    
        #Go ahead and make the adjustment if we're not going over the max center point.
        if self.viewport_center_y + what_to_add < self.viewport_center_max_y:
            self.update_viewport_center(self.viewport_center_x, self.viewport_center_y + what_to_add)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.viewport_center_x, self.viewport_center_max_y) 
        
    def subtract_from_viewport_y(self, what_to_subtract):
    
        #Go ahead and make the adjustment if we're not going under the min center point.
        if self.viewport_center_y - what_to_subtract > self.viewport_center_min_y:
            self.update_viewport_center(self.viewport_center_x, self.viewport_center_y - what_to_subtract)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.viewport_center_x, self.viewport_center_min_y)

    #When the zoom level is changed, several variables must be changed with it.
    def update_zoom_level(self, level):
    
        x, y = level
    
        self.zoom_area_width = x
        self.zoom_area_height = y
    
        self.viewport_center_min_x = self.zoom_area_width/2
        self.viewport_center_max_x = self.world_width - self.zoom_area_width/2

        self.viewport_center_min_y = self.zoom_area_height/2
        self.viewport_center_max_y = self.world_height - self.zoom_area_height/2
    
        #Test to see if viewport center is out of range after the the zoom, if so, fix'um up.  This can happen if you're at the edge of the screen and then zoom out - the center will be close to the edge.
        if self.viewport_center_x > self.viewport_center_max_x:
            self.viewport_center_x = self.viewport_center_max_x
        if self.viewport_center_x < self.viewport_center_min_x:
            self.viewport_center_x = self.viewport_center_min_x
        if self.viewport_center_y > self.viewport_center_max_y:
            self.viewport_center_y = self.viewport_center_max_y
        if self.viewport_center_y < self.viewport_center_min_y:
            self.viewport_center_y = self.viewport_center_min_y
           
        #Recalculate the other variables by calling update_viewport_center without changing the values of the center.
        self.update_viewport_center(self.viewport_center_x, self.viewport_center_y)
    
        #Redefine the size of the surface for the zoom_frame_buffer
        self.zoom_frame_buffer = pygame.surface.Surface(level).convert()
    
        #Redefine the size of the surface for the background
        self.background = pygame.surface.Surface(level).convert()
        self.background.fill((255, 255, 255))
        
        #Change the scroll_speed based on the zoom level.
        self.scroll_speed = self.scroll_speeds[self.zoom_level]
    
    
    #This function is called to do the final scaling of the image to fit the viewport/screen size.
    def finalize_image(self):
    
        #Let's take the zoom frame buffer and transform to the resolution of the screen and then copy it to the screen surface.
        pygame.transform.scale(self.zoom_frame_buffer, (global_data.screen_size_x, global_data.screen_size_y), self.surface)

    def change_zoom_level(self, direction):
    
        if direction == "in":
            if self.zoom_level > 0:
                self.zoom_level = self.zoom_level - 1
                self.update_zoom_level(self.zoom_levels[self.zoom_level])
        if direction == "out":
            if self.zoom_level < 5:
                self.zoom_level = self.zoom_level + 1
                self.update_zoom_level(self.zoom_levels[self.zoom_level])


#Mini_Map
class Mini_Map(viewport.Viewport):
    def __init__(self, x_right=0, y_down=0, width=256, height=256, world_width=1024, world_height=768):
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 0, True)

        self.world_width = world_width
        self.world_height = world_height
        
        self.x_scale_factor = float(self.world_width) / float(self.width)         #28.125
        self.y_scale_factor = float(self.world_height) / float(self.height)        #27.106
        
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        
        #Default for the mini map is not visable.  Not used yet.
        is_visable = False

        #For turning the minimap on and off effect.  
        self.scroll_x_right =self.x_right
        self.scroll_y_down = self.y_down
        # Scroll_state can moving on, moving off, on, or off.
        self.scroll_state = "off"
        
        #print str(self.x_scale_factor)
        #print str(self.y_scale_factor)
        
    def update(self, world):
        
        #Clear the mini map.
        self.surface.blit(self.background, (0, 0))
        #Let's go through all the entities and put them on the mini_map
        for entity in world.entities.itervalues():
            x_location, y_location = entity.location
            minimap_x = x_location/self.x_scale_factor
            minimap_y = y_location/self.y_scale_factor
            self.surface.set_at((int(minimap_x), int(minimap_y)), entity.color)
            pygame.draw.rect(self.surface, entity.color, (int(minimap_x), int(minimap_y), 2, 2))
            #print str(minimap_x), str(minimap_y), x_location, y_location
            
        # Scroll on or off the screen effect.
        # We're checking to see if we should be adjusting the location of the mini map.
        # How it works:
        # Check to see if it should be scrolling.  If so then:
        # Check to see if it's going up or down then:
        # Adjust self.top and self.left numbers below.
        
#        if self.scroll_state == "moving on":
#            self.scroll_y_down -= 1
#            if self.scroll_y_down <= self.y_down:
#                self.scroll_state = "on"
#            screen.blit(self.surface, (self.x_right, self.scroll_y_down))
#            print self.x_right, self.scroll_y_down
#        if self.scroll_state == "moving off":
#            self.scroll_y_down += 1 
#            if self.scroll_y_down >= self.y_down + self.height:
#                self.scroll_state = "off"
#            screen.blit(self.surface, (self.x_right, self.scroll_y_down))
#            print self.x_right, self.scroll_y_down, self.y_down + self.height
#        if self.scroll_state == "on":
#            screen.blit(self.surface, (self.x_right, self.y_down))
        #exit()
        #screen.blit(self.surface, (self.top, self.y_down))
    
    #Set up initial values to scroll the mini map onto the screen
    def turn_on(self):
        self.scroll_state = "moving on"
        #The starting position for y
        self.scroll_y_down = global_data.screen_size_y

        
    #Set up initial values to scroll the mini map off of the screen
    def turn_off(self):
        self.scroll_state = "moving off"
        self.scroll_y_down = self.y_down
        
    def delete_me(self):
        self.delete()
        del self
        #self = None