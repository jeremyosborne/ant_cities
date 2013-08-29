#Game specific UI element class definitions.
#Examples:  Mini-map.


import pygame
from pygame.locals import *

import viewport
import global_data

#This is our main game viewport.  It has a lot of custom code for this particular type of game, i.e. zooming and panning in a game world.
#So it doesn't belong in the main viewport class.
class World_Viewport(viewport.Viewport):
    def __init__(self, world_width, world_height, viewable_width, viewable_height):
        viewport.Viewport.__init__(self, 0, 0, viewable_width, viewable_height, 1, 0, True)
        
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
            
            #Code for keeping the aspect ratio on the viewport.
            #Making new copies of these because we might change them based on aspect ratio in the test further down.
            viewport_usable_width = self.zoom_area_width
            viewport_usable_height = self.zoom_area_height
            aspect_ratio_offset_width = 0
            aspect_ratio_offset_height = 0
            
            #Determine if adjustments based on aspect ratio are required.
            if (float(self.zoom_area_width) / float(self.zoom_area_height) - float(self.width) / float(self.height)) > .2:
                #Determine if it's width or height that's out of wack and then take proper action.
                viewport_aspect_ratio = float(self.width / self.height)
                zoom_area_aspect_ratio = float(self.zoom_area_width / self.zoom_area_height)
            
                #Should we go full width or height with the minimap based on the aspect ratio?  
                if (zoom_area_aspect_ratio >= 1) and (zoom_area_aspect_ratio >= viewport_aspect_ratio):
                    #Use width of the viewport.
                    viewport_usable_width = self.width
                    viewport_usable_height = self.zoom_area_height / float((self.zoom_area_width) / float(self.width))
                    #Calculate the offset of the viewport based on the aspect ratio.
                    aspect_ratio_offset_width = 0
                    aspect_ratio_offset_height = (self.height - viewport_usable_height) / 2
                else:
                    #Use height of the minimap.
                    viewport_usable_width = self.zoom_area_width / float((self.zoom_area_height) / float(self.height))
                    viewport_usable_height = self.height
                    #Calculate the offset of the viewport based on the aspect ratio.
                    aspect_ratio_offset_width = (self.width - viewport_usable_width) / 2
                    aspect_ratio_offset_height = 0
       
            
            print "viewport usable width, height: ", viewport_usable_width, viewport_usable_height
            #Determine scale factor.  Used in calculating position in the viewport.
            scale_factor_width = self.zoom_area_width/viewport_usable_width
            scale_factor_height = self.zoom_area_height/viewport_usable_height
            
            print "scale factors: ", scale_factor_width, scale_factor_height
            #Convert object's coordinates to the viewport we're drawing on.
            #Convert world coordinates to world viewable coordinates, then to viewport coordinates.
            x = (x - (self.world_viewable_center_x - self.zoom_area_width/2)) / scale_factor_width  + aspect_ratio_offset_width
            y = (y - (self.world_viewable_center_y - self.zoom_area_height/2)) / scale_factor_height + aspect_ratio_offset_height
            
            print x, y
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

    #This will be for special rendering, such as effects that no matter what zoom level you're at, you want to see.
    #The following code need to be modified to work with the new zoom rendering style.                 
    def force_render_entity(self, image, x, y):
        
        w, h = image.get_size()
        
        if self.viewport_rect.colliderect(pygame.Rect(x-w/2, y-h/2, w, h)):
            #We're in view.
            #Convert object's coordinates to the surface we're drawing on.
            x = x - (self.viewport_center_x - self.zoom_area_width/2)
            y = y - (self.viewport_center_y - self.zoom_area_height/2)
            self.zoom_frame_buffer.blit(image, (x-w/2, y-h/2)) 
        
    def update_viewport_center(self, x, y):
       
        self.world_viewable_center_x = x
        self.world_viewable_center_y = y
        self.world_viewable_x_rect = x - self.zoom_area_width/2
        self.world_viewable_y_rect = y - self.zoom_area_height/2
        self.world_viewable_rect = pygame.Rect(self.world_viewable_x_rect, self.world_viewable_y_rect, self.zoom_area_width, self.zoom_area_height)
    
    def add_to_viewport_x(self, what_to_add):
    
        #Go ahead and make the adjustment if we're not going over the max center point.
        if self.world_viewable_center_x + what_to_add < self.world_viewable_center_max_x:
            self.update_viewport_center(self.world_viewable_center_x + what_to_add, self.world_viewable_center_y) 
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.world_viewable_center_max_x, self.world_viewable_center_y)
        
    def subtract_from_viewport_x(self, what_to_subtract):
    
        #Go ahead and make the adjustment if we're not going under the min center point.
        if self.world_viewable_center_x - what_to_subtract > self.world_viewable_center_min_x:
            self.update_viewport_center(self.world_viewable_center_x - what_to_subtract, self.world_viewable_center_y)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.world_viewable_center_min_x, self.world_viewable_center_y)
             
    def add_to_viewport_y(self, what_to_add):
    
        #Go ahead and make the adjustment if we're not going over the max center point.
        if self.world_viewable_center_y + what_to_add < self.world_viewable_center_max_y:
            self.update_viewport_center(self.world_viewable_center_x, self.world_viewable_center_y + what_to_add)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.world_viewable_center_x, self.world_viewable_center_max_y) 
        
    def subtract_from_viewport_y(self, what_to_subtract):
    
        #Go ahead and make the adjustment if we're not going under the min center point.
        if self.world_viewable_center_y - what_to_subtract > self.world_viewable_center_min_y:
            self.update_viewport_center(self.world_viewable_center_x, self.world_viewable_center_y - what_to_subtract)
        else:
            #We might be scrolling with odd numbers, so let's go to the outmost edge.
            self.update_viewport_center(self.world_viewable_center_x, self.world_viewable_center_min_y)

    #When the zoom level is changed, several variables must be changed with it.
    def update_zoom_level(self, level):
    
        x, y = level
    
        self.zoom_area_width = x
        self.zoom_area_height = y
    
        self.world_viewable_center_min_x = self.zoom_area_width/2
        self.world_viewable_center_max_x = self.world_width - self.zoom_area_width/2

        self.world_viewable_center_min_y = self.zoom_area_height/2
        self.world_viewable_center_max_y = self.world_height - self.zoom_area_height/2
    
        #Test to see if viewport center is out of range after the the zoom, if so, fix'um up.  This can happen if you're at the edge of the screen and then zoom out - the center will be close to the edge.
        if self.world_viewable_center_x > self.world_viewable_center_max_x:
            self.world_viewable_center_x = self.world_viewable_center_max_x
        if self.world_viewable_center_x < self.world_viewable_center_min_x:
            self.world_viewable_center_x = self.world_viewable_center_min_x
        if self.world_viewable_center_y > self.world_viewable_center_max_y:
            self.world_viewable_center_y = self.world_viewable_center_max_y
        if self.world_viewable_center_y < self.world_viewable_center_min_y:
            self.world_viewable_center_y = self.world_viewable_center_min_y
           
        #Recalculate the other variables by calling update_viewport_center without changing the values of the center.
        self.update_viewport_center(self.world_viewable_center_x, self.world_viewable_center_y)
            
        #Change the scroll_speed based on the zoom level.
        self.scroll_speed = int (self.scroll_speed_init * 1.5 * self.current_zoom_level)

        self.print_debug()
        
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
        

#-------------------------------------------------------------------------------
#Mini_Map
class Mini_Map(viewport.Viewport):
    def __init__(self, x_right=0, y_down=0, width=256, height=256, world_width=1024, world_height=768):
        
        self.border_size = 10  #Made it 10 to match the screen scrolling width.
        self.border_color = (165,42,42)  #Brown
        
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 0, True)

        self.world_width = world_width
        self.world_height = world_height
                            
        self.minimap_width = self.width - self.border_size * 2
        self.minimap_height = self.height - self.border_size * 2
        
        #Adjust for minimap aspect ratio, world size vs minimap size.
        #Determine the aspect ratio of the minimap.
        self.minimap_aspect_ratio = float(self.minimap_width/self.minimap_height)
        #determine the aspect ratio of the world.
        self.world_aspect_ratio = float(self.world_width/self.world_height)
        
        #Should we go full width or height with the minimap based on the aspect ratio?  
        if (self.world_aspect_ratio >= 1) and (self.world_aspect_ratio >= self.minimap_aspect_ratio):
            #Use width of the minimap.
            self.minimap_usable_width = self.minimap_width
            self.minimap_usable_height = self.world_height / float((self.world_width) / float(self.minimap_width))
            #Calculate the offset of the minimap based on the aspect ratio.
            self.minimap_offset_width = 0
            self.minimap_offset_height = (self.minimap_height - self.minimap_usable_height) / 2
        else:
            #Use height of the minimap.
            self.minimap_usable_width = self.world_width / float((self.world_height) / float(self.minimap_height))
            self.minimap_usable_height = self.minimap_height
            #Calculate the offset of the minimap based on the aspect ratio.
            self.minimap_offset_width = (self.minimap_width - self.minimap_usable_width) / 2
            self.minimap_offset_height = 0
        
        self.x_scale_factor = float(self.world_width) / float(self.minimap_usable_width)
        self.y_scale_factor = float(self.world_height) / float(self.minimap_usable_height)

        #For debugging
        #print "self.minimap_usable_width and height: ", self.minimap_usable_width, self.minimap_usable_height
        #print "self.minimap_offset width and height: ", self.minimap_offset_width, self.minimap_offset_height
               
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill(self.border_color)
        self.minimap_surface = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background.fill((0, 0, 0))
        
        #Default for the mini map is not visable.  Not used yet.
        is_visable = False

        #For turning the minimap on and off effect.  
        #self.scroll_x_right =self.x_right
        #self.scroll_y_down = self.y_down
        # Scroll_state can moving on, moving off, on, or off.
        #self.scroll_state = "off"
        
        #print str(self.x_scale_factor)
        #print str(self.y_scale_factor)
        
    def update(self, world):
        
        #Clear the mini map.
        self.minimap_surface.blit(self.minimap_background, (0, 0))
        #Let's go through all the entities and put them on the mini_map
        for entity in world.entities.itervalues():
            x_location, y_location = entity.location
            minimap_x = x_location/self.x_scale_factor
            minimap_y = y_location/self.y_scale_factor
            #The following line would be useful for doing single pixels.
            #self.minimap_surface.set_at((int(minimap_x), int(minimap_y)), entity.color)
            #The following line draws the 2x2 square on the minimap using a rect.
            #pygame.draw.rect(self.minimap_surface, entity.color, (int(minimap_x), int(minimap_y), 2, 2))
            #The folling line draws the rect, but uses the fill method.  Trying here
            #because I read in the API documentation that fill would be hardware accelerated and rect isn't.
            self.minimap_surface.fill(entity.color, (int(minimap_x), int(minimap_y), 2, 2))
            
        #Let's put rectangle that shows what's in the gamewindow on the minimap.
        #For polygon
        point_pair_1 = (int(world.viewport.world_viewable_x_rect/self.x_scale_factor), int(world.viewport.world_viewable_y_rect/self.y_scale_factor))
        point_pair_2 = (int((world.viewport.world_viewable_x_rect+world.viewport.zoom_area_width)/self.x_scale_factor)-2,  int(world.viewport.world_viewable_y_rect/self.y_scale_factor))
        point_pair_3 = (int(world.viewport.world_viewable_x_rect/self.x_scale_factor), int((world.viewport.world_viewable_y_rect+world.viewport.zoom_area_height)/self.y_scale_factor)-2)
        point_pair_4 = (int((world.viewport.world_viewable_x_rect+world.viewport.zoom_area_width)/self.x_scale_factor)-2, int((world.viewport.world_viewable_y_rect+world.viewport.zoom_area_height)/self.y_scale_factor)-2)
        
        pygame.draw.polygon(self.minimap_surface, (255, 255, 0), (point_pair_1, point_pair_3, point_pair_4, point_pair_2), 2)
        
        #Put minimap together with the border with any offsets calculated for aspect ratio.
        self.surface.blit(self.background, (0, 0))
        self.surface.blit(self.minimap_surface, ((self.border_size + self.minimap_offset_width, self.border_size + self.minimap_offset_height)))
                            
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

#-------------------------------------------------------------------------------
# FPS display.
class FPS_Display(viewport.Viewport):
    def __init__(self):
        viewport.Viewport.__init__(self, 5, 5, 125, 20, 1, 10, True)
        self.font = pygame.font.SysFont("arial", 16);
        self.background = pygame.surface.Surface((125, 20)).convert()
        self.background.fill((255, 255, 255))
        #Make it such that when the surface is blitted on something else,
        #the background is transparent.
        self.surface.set_colorkey((255, 255, 255))
        
    def draw_fps(self, clock):
        fps = clock.get_fps()

        #Clear the surface.
        self.surface.blit(self.background, (0, 0))    

        label = self.font.render(str(fps), True, (0, 0, 0))
        self.surface.blit(label, (0, 0))

#-------------------------------------------------------------------------------            
#User Panel that contains game information.        
class User_Panel(viewport.Viewport):
    pass

