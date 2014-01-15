import pygame
from pygame import KEYDOWN, K_ESCAPE, K_TAB, K_q, K_m,\
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from events import EventPublisher, EventSubscriber
from commonmath import mmval



class UIController(EventPublisher, EventSubscriber):
    """Responsibilities:
    
    * Listen for events from the device, normalize and pass to view elements.
    * Provide a centralized location for logic shared among views.
    * Provide access to model and entity logic.
    """
    def __init__(self):
        super(UIController, self).__init__()
        
    def handle_event(self, event):
        """All events are passed to the UI Controller, and then will be passed
        on.
        
        Override to process events.
        
        event {pygame.event.Event} a raw pygame event object.
        """
        pass



class ZoomableViewportController(object):
    """Handles the logic of a constrained, zoomable view.
    """
    def __init__(self, min_zoom_dims, maximum_zoom_dims):
        
        # zoom-in/out factor per zoom level.
        self.zoom_factor = 1.5

        # List of zoom level dimensions.
        # Index == the zoom level (lower == more zoomed in)
        # Dimensions are a tuple (width, height) of pixels viewable.
        self.zoom_level_dims = []

        self.maximim_zoom_dims = maximum_zoom_dims

        # Calculate the zoom levels.
        self.create_zoom_level_dims(min_zoom_dims, maximum_zoom_dims)

        # The currently visible area.
        self.rect = pygame.Rect(0, 0, 0, 0)

        # {int} Default zoom level (needs to be done after zoom level calculation).
        self.zoom_level = len(self.zoom_level_dims)-1
        
    @property
    def zoom_level(self):
        """{int} The current zoom level.
        """
        return self._zoom_level
    
    @zoom_level.setter
    def zoom_level(self, value):
        """{int}
        """
        # Boundary check.
        self._zoom_level = mmval(len(self.zoom_level_dims)-1, value, 0)

        # Resize the viewable area.
        self.rect.width = self.zoom_area_width
        self.rect.height = self.zoom_area_height
        
        # Correct the center point.
        self.move(*self.rect.center)
    
    @property
    def zoom_area_width(self):
        """Width in pixels at the current zoom level.
        """
        return self.zoom_level_dims[self.zoom_level][0]

    @property
    def zoom_area_height(self):
        """Height in pixels at the current zoom level.
        """
        return self.zoom_level_dims[self.zoom_level][1]

    def create_zoom_level_dims(self, min_zoom_dims, maximum_zoom_dims):
        """Populates the zoom_level_dims list.
        
        min_zoom_dims {tuple} (width, height) pixel size of our lowest
        level.
        maximim_zoom_dims {tuple} (width, height) pixel size of our highest
        zoom level.
        """
        
        # Remove if and when we want this to be called more than once.
        assert len(self.zoom_level_dims) == 0, "Function should be called only once."
        
        # Default zoom level no scaling.
        self.zoom_level_dims.append(min_zoom_dims)
        
        # Calculate the remaining levels.
        while True:
            # Keep building zoom levels until the max zoom level encompasses the
            # entire game world.
            prev_zoom_level = self.zoom_level_dims[-1]
            next_zoom_level = (prev_zoom_level[0]*self.zoom_factor, 
                               prev_zoom_level[1]*self.zoom_factor)
            if ((next_zoom_level[0] <= maximum_zoom_dims[0]) and (next_zoom_level[1] <= maximum_zoom_dims[1])):
                self.zoom_level_dims.append(next_zoom_level)
            else:
                # Final zoom level. Make it match the size of the game world
                # even if it's not full factor zoom.
                self.zoom_level_dims.append(maximum_zoom_dims)
                break

        if __debug__:
            print "Zoom level ranges (%s total zoom levels)" % len(self.zoom_level_dims)
            print self.zoom_level_dims

    def scroll(self, x=0, y=0):
        """Scrolls the viewport relative to its current position.
        
        (x, y) are offsets applied as a delta to the current position of the
        center.
        
        """
        # Convenience method, handoff to move.
        self.move(self.rect.centerx+x, self.rect.centery+y)
    
    def move(self, x=None, y=None):
        """Moves the viewport and adjusts the dimensions of the bounding
        rectangle.
        
        (x, y) make up the new center coordinate for the viewport.
        
        Needs to be called to to after zoom level changes, too.
        """
        
        max_width = self.maximim_zoom_dims[0]
        max_height = self.maximim_zoom_dims[1]
        
        # Default to the center of the largest view.
        x = x if x != None else max_width/2
        y = y if y != None else max_height/2

        # Test to see if viewport center is out of range after the the zoom, 
        # if so, fix'um up.  This can happen if you're at the edge of the 
        # screen and then zoom out - the center will be close to the edge.
        x = mmval(max_width - self.zoom_area_width/2, x, self.zoom_area_width/2)
        y = mmval(max_height - self.zoom_area_height/2, y, self.zoom_area_height/2)

        # Update the visible area.
        self.rect.center = (x, y)



class GameUIController(UIController):
    """Manages pass through of logic between device and simulation and the
    visual elements.
    """
    
    # {Entity} What entity or entities are selected?
    entity_selection = None
    # {bool} Should we track the entity?
    entity_selection_track = False

    # {tuple} (x,y) Mouse coordinates as device pixel coordinates.
    mouse_screenxy = (0, 0)

    # {tuple} (x,y) Mouse coordinates translated to game world coordinates.
    mouse_worldxy = (0, 0)
    
    def __init__(self, game_engine):
        super(GameUIController, self).__init__()
        
        # The global game_engine.
        self.game_engine = game_engine
        
        # The height and width of the world.
        self.world = game_engine.world
        
        # Reference to the main image cache.
        self.imageassets = game_engine.imageassets
        
        # Defines the viewable portion of the entire world.
        # Keep the default dimensions the size of the map.
        # Max pixel size == max size of the world.
        min_zoom_dims = game_engine.globaldata.SCREEN_SIZE[0], game_engine.globaldata.SCREEN_SIZE[1]-170
        max_zoom_dims = game_engine.world.width, game_engine.world.height
        self.world_viewport = ZoomableViewportController(min_zoom_dims, max_zoom_dims)

    @property
    def fps(self):
        """{float} What is the current calculated fps?
        """
        return round(self.game_engine.clock.get_fps(), 1)

    def handle_event(self, event):
        """Passed all events from pygame.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Quit.
                return
            if event.key == K_TAB:
                # Grab the mouse
                pygame.event.set_grab(not pygame.event.get_grab())
        elif event.type == MOUSEBUTTONDOWN:
            self.pub("MOUSEBUTTONDOWN", ev=event)
        elif event.type == MOUSEBUTTONUP:
            self.pub("MOUSEBUTTONUP", ev=event)
        elif event.type == MOUSEMOTION:
            self.pub("MOUSEMOTION", ev=event)

    def process(self, time_passed):
        """Called once per tick to update general UI things.
        """
        # Mouse coordinates right now.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Publish the screen coordinates each tick.
        self.mouse_screenxy = (mouse_x, mouse_y)
        
        #----------------------------------------------------------------------
        # Scroll the map if mouse is near the edge of the screen.
        # Number of pixel buffer from the edges of the window in which we will scroll.
        scroll_buffer = 20
        # How many visual pixels do we move per frame when scrolling?
        scroll_speed_multiplier = 20
        # References to items.
        world_viewport = self.world_viewport
        display = self.game_engine.display
        # Scroll speed of view (in pixels)
        scroll_speed = (world_viewport.zoom_level+1)*world_viewport.zoom_factor*scroll_speed_multiplier
        if mouse_x >= 0 and mouse_x <= scroll_buffer:
            world_viewport.scroll(x=-scroll_speed)
        elif (mouse_x >= display.width-scroll_buffer) and mouse_x <= display.width:
            world_viewport.scroll(x=scroll_speed)
        if mouse_y >= 0 and mouse_y <= scroll_buffer:
            world_viewport.scroll(y=-scroll_speed)
        elif (mouse_y >= display.height-scroll_buffer) and mouse_y <= display.height:
            world_viewport.scroll(y=scroll_speed)
        #----------------------------------------------------------------------

    
        