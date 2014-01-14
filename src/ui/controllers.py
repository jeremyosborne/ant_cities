import pygame
from pygame import KEYDOWN, K_ESCAPE, K_TAB, K_q, K_m,\
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from events import EventPublisher, EventSubscriber



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



class GameUIController(UIController):
    """Manages pass through of logic between device and simulation and the
    visual elements.
    """
    
    # {Entity} What entity or entities are selected?
    entity_selection = None
    # {bool} Should we track the entity?
    entity_selection_track = False

    # {tuple} (x,y) Mouse coordinates translated to game world coordinates.
    mouse_worldxy = (0, 0)
    
    def __init__(self, game_simulation):
        super(GameUIController, self).__init__()
        
        # The global game_simulation.
        self.game_simulation = game_simulation
        
        # The height and width of the world.
        self.world = game_simulation.world
        
    def handle_event(self, event):
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

    @property
    def fps(self):
        """{float} What is the current calculated fps?
        """
        return round(self.game_simulation.clock.get_fps(), 1)
    
        