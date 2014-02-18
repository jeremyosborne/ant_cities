"""This is a layout focused module.

Complex views should be defined elsewhere.
"""

from common.ui.pygameview import PygameView
from ui.datacolumndisplay import DataColumnDisplay
from ui.unitinfobox import UnitInfoBox
from ui.minimap import MiniMap



class PlayerBaseInfo(DataColumnDisplay):
    def subclass_init(self, **kwargs):
        pinfo = self.controller.player_info_controller
        t = self.controller.player_info_controller.team_name
        d = [
            ("Game Time:", lambda: str(pinfo.game_time_passed)),
            ("Ants:", lambda: str(pinfo.entity_population)),
            ("Energy:", lambda: str(pinfo.anthill_energy)),
        ]
        super(PlayerBaseInfo, self).subclass_init(title=t, data=d)
        
    def position(self):
        # Positioned in upper left of control panel.
        self.scale_relative_to_parent(0.167, 1)



class ControlPanelUnitInfoBox(UnitInfoBox):
    def position(self):
        self.scale_relative_to_parent(0.213, 1)
        # TODO: Need a positionable relative to sibling (maybe an align relative
        # to, or something like that).
        self.position_relative_to_parent(self.controller.display.width-512, "top")



class ControlPanelMiniMap(MiniMap):
    def position(self):
        self.scale_relative_to_parent(.213, 1)
        self.position_relative_to_parent("right", "bottom")


    
class ControlPanel(PygameView):
    def subclass_init(self, **kwargs):
        self.addchild(PlayerBaseInfo(controller=self.controller))
        self.addchild(ControlPanelUnitInfoBox(controller=self.controller))
        self.addchild(ControlPanelMiniMap(controller=self.controller))
        
    def position(self):
        self.scale_relative_to_parent(1, 0.25)
        self.position_relative_to_parent("left", "bottom")
        # Position all children.
        # TODO: This should become the standard when positioning a parent
        # PygameView
        for c in self.childviews:
            c.position()

