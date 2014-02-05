import pygame

import globaldata
from world import World
from ui.minimap import MiniMap
from ui.unitinfobox import UnitInfoBox
from ui.fpsdisplay import FPSDisplay
from ui.datacolumndisplay import DataColumnDisplay
from ui.map import Map
from ui.mousedisplay import MouseDisplay
from ui.controllers import GameUIController
from ui.assets.gameassets import GameAssets
from ui.pygameview import PygameDisplay, PygameView


class GameEngine():
    """The main game object, responsible for running the simulation and the
    ui.
    """
    def __init__(self):
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
        control_panel = PygameView(controller=self.ui_controller)
        self.display.addchild(control_panel)
        control_panel.scale_relative_to_parent(1, 0.25)
        control_panel.position_relative_to_parent("left", "bottom")

        # Player Base Information
        data_to_display = [
            ("Game Time:", lambda: str(self.ui_controller.player_info_controller.game_time_passed)),
            ("Ants:", lambda: str(self.ui_controller.player_info_controller.entity_population)),
            ("Energy:", lambda: str(self.ui_controller.player_info_controller.anthill_energy)),
        ]
        player_base_info = DataColumnDisplay(title=self.ui_controller.player_info_controller.team_name,
                                            data=data_to_display)
        control_panel.addchild(player_base_info)
        player_base_info.scale_relative_to_parent(0.167, 1)

        # Unit information display.
        # TODO: Need a positionable relative to sibling (maybe an align relative
        # to, or something like that).
        unit_info_box = UnitInfoBox(controller=self.ui_controller)
        control_panel.addchild(unit_info_box)
        unit_info_box.scale_relative_to_parent(0.213, 1)
        unit_info_box.position_relative_to_parent(self.display.width-512, "top")

        mini_map = MiniMap(controller=self.ui_controller)
        control_panel.addchild(mini_map)
        mini_map.scale_relative_to_parent(.213, 1)
        mini_map.position_relative_to_parent("right", "bottom")
        
        

    def process(self):

        # Time_passed is in milliseconds.
        time_passed = self.clock.tick(60)
        
        # Update logic.
        self.world.process(time_passed)
        
        self.ui_controller.process(time_passed)

        # Update UI.
        self.display.render()
