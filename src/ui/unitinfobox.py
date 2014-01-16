import pygame
from ui.pygameview import PygameView



class ToggleButton(PygameView):
    """Toggle button.
     
    Experimental: things specific to the UnitInfoBox are hardcoded.
    """
    def subclass_init(self, **kwargs):
        self.xpos = kwargs.get("xpos", "left")
        self.ypos = kwargs.get("ypos", "top")
        self.buf = kwargs.get("buf", 0)
        
        onsurface = kwargs.get("onsurface", "track-enabled")
        self.onsurface = self.controller.game_assets.image(onsurface)
        offsurface = kwargs.get("offsurface", "track-disabled")
        self.offsurface = self.controller.game_assets.image(offsurface)

        # Register event listeners.
        self.events_sub()

    def events_sub(self):
        self.subto(self.controller, "MOUSEBUTTONDOWN", self.mousebuttondown_listener)

    def position_after_add(self):
        """This is a stupid function name.
        """
        self.position_relative_to_parent(self.xpos, self.ypos, self.buf)

    def draw(self, surface):
        # If we do have an entity selected, give the option to track.
        if self.controller.entity_selection_track == True:
            surface.blit(self.onsurface, (self.x, self.y))            
        else:
            surface.blit(self.offsurface, (self.x, self.y))

    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        # Taking care of the tracking button toggle.
        if event.button == 1 and self.contained_screenxy(event.pos) is True:
            # Toggle.
            self.controller.entity_selection_track = not self.controller.entity_selection_track



class UnitInfoBox(PygameView):
    """Info display about selected unit.
    """
    def subclass_init(self, **kwargs):
        self.font = pygame.font.SysFont("arial", 16)

        # Prepare the static background.
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        label = self.font.render("Unit Info", True, (255, 255, 255))
        w, _ = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        # Do we need a permanent reference to the tracking button?
        toggle_button = ToggleButton(width=30, height=30, xpos="right", buf=5,
                                   controller=self.controller,
                                   onsurface="track-enabled",
                                   offsurface="track-disabled")
        self.addchild(toggle_button)
        # Ugg... probably need a positioning interface for when a view is
        # added and _after_ it has acquired its parent for relative positioning.
        toggle_button.position_after_add()
    
    def clear(self):
        self.surface.blit(self.background, (0, 0))
        
    def draw(self, surface):
        """Display information about a selected unit, if there is one.
        """
        ent = self.controller.entity_selection

        # If we have not selected an entity.
        if not ent:
            self.surface.blit(self.background, (0, 0))
            self.controller.entity_selection_track = False
            return
            
        # And provide details about the unit.
        unit_text = self.font.render("%s (id: %s)" % (ent.name, ent.id), True, (255, 255, 255))
        w, _ = unit_text.get_size()
        self.surface.blit(unit_text, ((self.width / 2) - w / 2, 15))
        
        output = ["Location: (%d, %d)" % tuple(ent.location)]

        if ent.name == "ant":
            output.append("Energy: %s" % ent.c["attrs"]["energy"])
            output.append("Health: %s" % ent.c["attrs"]["health"])
            output.append("Brain state: %s" % ent.brain.active_state.name)
            output.append("Speed: %d" % ent.c["velocity"].speed)
            if ent.c["destination"].location:
                output.append("Destination: (%s, %s)" % tuple(ent.c["destination"].location))
            if ent.c["destination"].isentity:
                output.append("Target: (%s)" % ent.c["destination"].val.name)
            
        for i, line in enumerate(output):
            text = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text, (10, 30 + i*15))
        
        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))
    