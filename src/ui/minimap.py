import pygame
import viewport
from assets.colors import entity_colors

class MiniMap(viewport.Viewport):
    def __init__(self, x_right=0, y_down=0, width=256, height=256, 
                 world_width=1024, world_height=768, controller=None):
        """Arguments not inherited from viewport.
        
        controller {EventPublisher} Provides a pipeline to events in the outside
        world.
        """
        
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 0, True)

        self.border_size = 10  #Made it 10 to match the screen scrolling width.
        self.border_color = (165,42,42)  #Brown

        self.description = "Mini Map"

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
        
        #Scale factors for translating mouse clicks inside the minimap.
        #self.mouse_x_scale_factor = float(self.)
               
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill(self.border_color)
        self.minimap_surface = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background = pygame.surface.Surface((self.minimap_usable_width, self.minimap_usable_height)).convert()
        self.minimap_background.fill((0, 0, 0))
        
        # Panning of the map is active.
        self.panning_map = False

        # Register event listeners.
        if controller is not None:
            controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
            controller.sub("MOUSEBUTTONUP", self.mousebuttonup_listener)
            controller.sub("MOUSEMOTION", self.mousemotion_listener)
        elif __debug__:
            print "WARNING: controller was not defined, no event listening will be happening in", self

        # For debugging
        if __debug__:
            print "MiniMap instance property values"
            print "minimap_usable_width and height: ", self.minimap_usable_width, self.minimap_usable_height
            print "minimap_offset width and height: ", self.minimap_offset_width, self.minimap_offset_height        

    def update(self, world, world_viewport, draw=True):
        """Update the mini view of the game world.
        
        world {World} Gameworld reference.
        world_viewport {WorldViewport} Gameworld viewable reference.
        [draw] {bool} Override to allow temporary non-drawing of minimap.
        """
        if not draw:
            return

        # Clear the mini map.
        self.minimap_surface.blit(self.minimap_background, (0, 0))
        # Let's go through all the entities and put them on the mini_map
        for entity in world.entities.itervalues():
            x_location, y_location = entity.location
            minimap_x = x_location/self.x_scale_factor
            minimap_y = y_location/self.y_scale_factor
            # The following line would be useful for doing single pixels.
            #self.minimap_surface.set_at((int(minimap_x), int(minimap_y)), entity.color)
            # The following line draws the 2x2 square on the minimap using a rect.
            #pygame.draw.rect(self.minimap_surface, entity.color, (int(minimap_x), int(minimap_y), 2, 2))
            # The following line draws the rect, but uses the fill method.  Trying here
            # because I read in the API documentation that fill would be hardware accelerated and rect isn't.
            self.minimap_surface.fill(entity_colors(entity), (int(minimap_x), int(minimap_y), 2, 2))
            
        #Let's put rectangle that shows what's in the gamewindow on the minimap.
        #For polygon
        point_pair_1 = (int(world_viewport.world_viewable_rect.left/self.x_scale_factor), 
                        int(world_viewport.world_viewable_rect.top/self.y_scale_factor))
        point_pair_2 = (int((world_viewport.world_viewable_rect.left+world_viewport.zoom_area_width)/self.x_scale_factor)-2,  
                        int(world_viewport.world_viewable_rect.top/self.y_scale_factor))
        point_pair_3 = (int(world_viewport.world_viewable_rect.left/self.x_scale_factor), 
                        int((world_viewport.world_viewable_rect.top+world_viewport.zoom_area_height)/self.y_scale_factor)-2)
        point_pair_4 = (int((world_viewport.world_viewable_rect.left+world_viewport.zoom_area_width)/self.x_scale_factor)-2, 
                        int((world_viewport.world_viewable_rect.top+world_viewport.zoom_area_height)/self.y_scale_factor)-2)
        
        pygame.draw.polygon(self.minimap_surface, (255, 255, 0), (point_pair_1, point_pair_3, point_pair_4, point_pair_2), 2)
        
        #Put minimap together with the border with any offsets calculated for aspect ratio.
        self.surface.blit(self.background, (0, 0))
        self.surface.blit(self.minimap_surface, ((self.border_size + self.minimap_offset_width, self.border_size + self.minimap_offset_height)))

    def mousebuttondown_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = True
    
    def mousemotion_listener(self, e):
        if self.panning_map == True:
            game_simulation = e.data["game_sim"]
            
            viewport_mouse_x, viewport_mouse_y = self.screenxy_to_relativexy(e.data["ev"].pos)
            
            # Define a rect that matches the actual area on the viewport 
            # where the minimap is, i.e. don't count the borders.
            minimap_rect = pygame.Rect(self.border_size + self.minimap_offset_width, self.border_size + self.minimap_offset_height, self.minimap_usable_width, self.minimap_usable_height)

            if minimap_rect.collidepoint(viewport_mouse_x, viewport_mouse_y) == True:
                # Adjust mouse coordinates to match the viewport map.
                viewport_mouse_x = viewport_mouse_x - self.minimap_offset_width - self.border_size
                viewport_mouse_y = viewport_mouse_y - self.minimap_offset_height - self.border_size
                                
                # Convert into gameworld coordinates.
                gameworld_x = int(viewport_mouse_x * self.x_scale_factor)
                gameworld_y = int(viewport_mouse_y * self.y_scale_factor)

                # Change centerpoint of the map.
                game_simulation.world_viewport.move_viewport(gameworld_x, gameworld_y)

    def mousebuttonup_listener(self, e):
        if e.data["ev"].button == 1:
            self.panning_map = False

