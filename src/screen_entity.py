"""
An class for implementing a viewport.
"""

import pygame
from pygame.locals import *

import global_data


class Screen_Entity(object):
    """Manages various viewport abstractions."""
    def __init__(self, top=0, left=0, width=1024, height=768, scale=1, layer=0, is_visable=True):
        """Arguments assumed to be integers."""
        # The upper left anchor point of our viewport [left, top]
        self.anchor = [top, left]
        # The dimensions of our viewport as [width, height]
        # Assumed width and height are positive.
        self.size = [width, height]
        # Scales relative to 1 as default.
        self.scale = scale
        #The surface for this screen entity.
        self.surface = pygame.surface.Surface(self.size).convert()
        #Layer, can be though of as the sequence of blitting.  0 is the lowest layer.
        self.layer = layer
        #Should is be rendered?
        self.is_visable=is_visable 

    @property
    def top(self):
        """{int} The relative top coordinate offset."""
        return self.anchor[1]
    
    @top.setter
    def top(self, value):
        self.anchor[1] = value
    
    @property
    def left(self):
        """{int} The relative left coordinate offset."""
        return self.anchor[0]
    
    @left.setter
    def left(self, value):
        self.anchor[0] = value
    
    @property
    def right(self):
        """{int} The relative right coordinate (offset + width)."""
        return self.anchor[0] + self.size[0]

    @property
    def bottom(self):
        """{int} The relative bottom coordinate (offset + height)."""
        return self.anchor[1] + self.size[1]
    
    @property
    def width(self):
        return self.size[0]
    
    @width.setter
    def width(self, value):
        self.size[0] = value
    
    @property
    def height(self):
        return self.size[1]
    
    @height.setter
    def height(self, value):
        self.size[1] += value

    #Render this Screen Entity into whatever surface is passed in.    
    def render(self, main_surface):
        main_surface.blit(self.surface, ((self.top, self.left)))

class World_Screen_Entity(Screen_Entity):
    def __init__(self):
        Screen_Entity.__init__(self, 0, 0, global_data.screen_size_x, global_data.screen_size_y, 1, 0, True)

        self.zoom_area_width = global_data.screen_size_x
        self.zoom_area_height = global_data.screen_size_y

        #Hard coded Zoom level for testing
        #Zoom levels as tuples.
        self.zoom_level_1 = (global_data.screen_size_x/2, global_data.screen_size_y/2)
        self.zoom_level_2 = (global_data.screen_size_x, global_data.screen_size_y)
        self.zoom_level_3 = (global_data.screen_size_x+global_data.screen_size_x/2, global_data.screen_size_y+global_data.screen_size_y/2)
        self.zoom_level_4 = (global_data.screen_size_x*2, global_data.screen_size_y*2)
        self.zoom_level_5 = (global_data.screen_size_x*3, global_data.screen_size_y*3)
        #List of tuples representing the zoom levels
        self.zoom_levels = (self.zoom_level_1, self.zoom_level_2, self.zoom_level_3, self.zoom_level_4, self.zoom_level_5)

        #default zoom level
        self.zoom_level = 2

        #Scroll speeds that will be used based on zoom level
        self.scroll_speeds = (5, 10, 20, 40, 60)
        #default scroll speed
        self.scroll_speed = 10

        self.viewport_center_x = global_data.world_size_x / 2
        self.viewport_center_min_x = self.zoom_area_width/2
        self.viewport_center_max_x = global_data.world_size_x - self.zoom_area_width/2
        self.viewport_center_y = global_data.world_size_y / 2
        self.viewport_center_min_y = self.zoom_area_height/2
        self.viewport_center_max_y = global_data.world_size_y - self.zoom_area_height/2

        #Defining the rectangle of the viewport
        self.viewport_x_rect = self.viewport_center_x - self.zoom_area_width/2
        self.viewport_y_rect = self.viewport_center_y - self.zoom_area_height/2
        self.viewport_rect = pygame.Rect(self.viewport_x_rect, self.viewport_y_rect, self.zoom_area_width, self.zoom_area_height)

        #The zoom_frame_buffer is the surface where everything is rendered (blited) to.  It will then be scaled to fit the viewport.
        self.zoom_frame_buffer = pygame.surface.Surface((self.zoom_area_width, self.zoom_area_height)).convert()


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

    def render(self, surface):
        pygame.transform.scale(self.zoom_frame_buffer, (global_data.screen_size_x, global_data.screen_size_y), surface)

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
        self.viewport_center_max_x = global_data.world_size_x - self.zoom_area_width/2

        self.viewport_center_min_y = self.zoom_area_height/2
        self.viewport_center_max_y = global_data.world_size_y - self.zoom_area_height/2
    
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
        #background = pygame.surface.Surface(level).convert()
    
        #Change the scroll_speed based on the zoom level.
        self.scroll_speed = self.scroll_speeds[self.zoom_level]
    
    
    #This function is called to do the final scaling of the image to fit the viewport/screen size.
    def finalize_image(self, surface):
    
        #Let's take the zoom frame buffer and transform to the resolution of the screen and then copy it to the screen surface.
        pygame.transform.scale(self.zoom_frame_buffer, (global_data.screen_size_x, global_data.screen_size_y), surface)

    def change_zoom_level(self, direction):
    
        if direction == "in":
            if self.zoom_level > 0:
                self.zoom_level = self.zoom_level - 1
                self.update_zoom_level(self.zoom_levels[self.zoom_level])
        if direction == "out":
            if self.zoom_level < 4:
                self.zoom_level = self.zoom_level + 1
                self.update_zoom_level(self.zoom_levels[self.zoom_level])














if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((1024,768), 0, 32)
        
    print "Testing..."
    v = Screen_Entity()
    print "Initial viewport width: %s" % v.width
    print "Left anchor: %s" % v.left
    print "Right anchor: %s" % v.right
    print "Changing left anchor point by 100."
    v.left = 100
    print "Left anchor: %s" % v.left
    print "Right anchor: %s" % v.right

    print "Initial viewport height: %s" % v.height
    print "Top anchor: %s" % v.top
    print "Bottom anchor: %s" % v.bottom
    print "Changing top anchor point by 100."
    v.top = 100
    print "Top anchor: %s" % v.top
    print "Bottom anchor: %s" % v.bottom
