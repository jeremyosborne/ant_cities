import pygame

import globaldata
from world import World
from ui.assets import GameAssets
from ui.controllers import GameUIController
from ui.map import Map
from ui.fpsdisplay import FPSDisplay
from ui.mousedisplay import MouseDisplay
from common.ui.pygameview import PygameDisplay
from ui.controlpanel import ControlPanel



class GameEngine():
    """The main game object, responsible for running the simulation and the
    ui.
    """
    def __init__(self):
        
        # This initialization needs to be done before other pygame calls.
        pygame.init()
        pygame.display.set_caption(globaldata.GAME_TITLE)
        
        # Reference to the globaldata for our application.
        self.globaldata = globaldata
        
        # Reference to the game clock for handling framerate.
        self.clock = pygame.time.Clock()
        
        self.world = World(globaldata.WORLD_SIZE[0], globaldata.WORLD_SIZE[1])

        # -------------------------------------------- UI
        
        # Cache of image assets.
        self.game_assets = GameAssets(globaldata.ASSETS_PATH)

        # The main display, which all other views should be nested with.
        # Display needs to be set before any graphics calls and the main
        # UI controller.
        self.display = PygameDisplay(globaldata.SCREEN_SIZE[0], globaldata.SCREEN_SIZE[1])

        # Controller for all UI elements.
        self.ui_controller = GameUIController(self)

        # Map scales itself to the screensize.
        self.display.addchild(Map(controller=self.ui_controller))

        # TODO: Should have a debug panel, and the following two things should
        # be added.        
        # Frames per second.
        self.display.addchild(FPSDisplay(5, 5, controller=self.ui_controller))
        # Mouse coordinates.
        self.display.addchild(MouseDisplay(5, 25, controller=self.ui_controller))


        # On screen player controls and information readouts.
        self.display.addchild(ControlPanel(controller=self.ui_controller))
        
    def process(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)
        
        # Update logic.
        self.world.process(time_passed)
        
        self.ui_controller.process(time_passed)

        # Update UI.
        self.display.render()

    def run(self):
        """Call to start the game.
        """
        
        if __debug__:
            print pygame.display.Info()
    
        # Main game loop.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    self.ui_controller.handle_event(event)
            
            self.process()
