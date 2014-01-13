from events import EventPublisher, EventSubscriber
import pygame
from pygame import KEYDOWN, K_ESCAPE, K_TAB, K_q, K_m,\
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION


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
    
    def __init__(self, game_simulation):
        super(GameUIController, self).__init__()
        self.game_simulation = game_simulation
        
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
