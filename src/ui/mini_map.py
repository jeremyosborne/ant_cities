import pygame
import viewport

class Mini_Map(viewport.Viewport):
    def __init__(self, x_right=0, y_down=0, width=256, height=256, world_width=1024, world_height=768):
        
        self.description = "Mini Map"
        
        self.mouse_events = True
        
        self.border_size = 10  #Made it 10 to match the screen scrolling width.
        self.border_color = (165,42,42)  #Brown
        
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 0, True)

        self.world_width = world_width
        self.world_height = world_height
                            
        self.minimap_width = self.width - self.border_size * 2
        self.minimap_height = self.height - self.border_size * 2
        
        self.description = "Mini-Map display."
        
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
        
        #Scale factors for translating mouse clicks inside the minimap.
       # self.mouse_x_scale_factor = float(self.)

        #For debugging
        print "self.minimap_usable_width and height: ", self.minimap_usable_width, self.minimap_usable_height
        print "self.minimap_offset width and height: ", self.minimap_offset_width, self.minimap_offset_height
               
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill(self.border_color)
        self.minimap_surface = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background.fill((0, 0, 0))
        

        
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
                            
        
    def delete_me(self):
        self.delete()
        del self
        #self = None

    def service_user_event(self, event, game_simulation):
        
        #Let's take care of the left mouse button.  A left mouse click in this window
        #recenters the game world view.
        
        if event.button == 1:  #left click.
            
            #When we detect the mouse up event, we'll set the following to False and end
            #the loop.  All user events except for mouse scrolling and zooming are being 
            #directed to only this method.
            mouse_button_is_down = True
            
            while mouse_button_is_down:
                #Convert the global x and y coordinates of the mouse to the viewport.  Note
                #that this is not adjusted to the minimap, just the viewport containing the
                #actual map and map borders.
                mouse_x, mouse_y = pygame.mouse.get_pos()            
                viewport_mouse_x = mouse_x - self.x_right
                viewport_mouse_y = mouse_y - self.y_down
                
                #Define a rect that matches the actual area on the viewport where the minimap is, i.e. don't count the borders.
                minimap_rect = pygame.Rect(self.border_size + self.minimap_offset_width, self.border_size + self.minimap_offset_height, self.minimap_usable_width, self.minimap_usable_height )
    
                if minimap_rect.collidepoint(viewport_mouse_x, viewport_mouse_y) == True:
                    #Adjust mouse coordinates to match the viewport map.
                    viewport_mouse_x = viewport_mouse_x - self.minimap_offset_width - self.border_size
                    viewport_mouse_y = viewport_mouse_y - self.minimap_offset_height - self.border_size
                                    
                    #Convert into gameworld coordinates.
                    gameworld_x = int(viewport_mouse_x * self.x_scale_factor)
                    gameworld_y = int(viewport_mouse_y * self.y_scale_factor)

                    #Change centerpoint of the map
                    game_simulation.world.viewport.update_viewport_center(gameworld_x, gameworld_y)

            
                #Process the game world.  We want things to keep going.
                game_simulation.process_game_loop()
                
                #Let's check to see if the mouse_up_event has happened yet, if so, it's time to exit this loop.
                #We only look at one at a time.
                new_event = pygame.event.poll()
                if new_event.type == pygame.MOUSEBUTTONUP and new_event.button == 1:
                    mouse_button_is_down = False
