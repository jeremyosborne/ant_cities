import pygame
import ui.viewport as viewport

class UnitInfoBox(viewport.Viewport):
    """Traditional area that displays information about a single unit a user has clicked on.
    """
    def __init__(self, x=0, y=0, width=256, height=256, 
                 controller=None, imageassets=None):
        """Arguments not inherited from viewport.
        
        controller {EventPublisher} Provides a pipeline to events in the outside
        world.
        imageassets {AssetCache} Image cache.
        """

        viewport.Viewport.__init__(self, x, y, width, height)

        self.font = pygame.font.SysFont("arial", 16)
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))

        # Add title to the background image.
        label = self.font.render("Unit Info", True, (255, 255, 255))
        w, _ = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        pygame.draw.line(self.background, (255, 255, 255), (0, 0), (0, self.height), 10)
        
        self.surface.blit(self.background, (0, 0))

        # Toggle for tracking the entity on screen.
        self.track = False
        
        #Load Button Icons
        self.Start_Tracking_Button = imageassets.load("track-enable")
        self.Stop_Tracking_Button = imageassets.load("track-disable")
                
        # Register event listeners.
        self.controller = controller
        controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        
    def draw_view(self, surface):
        """Display information about a selected unit, if there is one.
        """
        ent = self.controller.entity_selection
        
        self.surface.blit(self.background, (0, 0))
        
        # If we have not selected an entity.
        if not ent:
            self.surface.blit(self.background, (0, 0))
            self.track = False
            return

        # If we do have an entity selected, give the option to track.
        if self.controller.entity_selection_track == True:
            self.surface.blit(self.Start_Tracking_Button, (self.width - 30, 0))            
        else:
            self.surface.blit(self.Stop_Tracking_Button, (self.width -30, 0))
            
        # And provide details about the unit.
        unit_text = self.font.render(ent.name, True, (255, 255, 255))
        w, _ = unit_text.get_size()
        self.surface.blit(unit_text, ((self.width / 2) - w / 2, 15))
        
        output = ["Location: (%d, %d)" % tuple(ent.location)]

        if ent.name == "ant":
            output.append("Energy: %s" % ent.c["energy"].val)
            output.append("Health: %s" % ent.c["health"].val)
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
        
    def mousebuttondown_listener(self, e):
        event = e.data["ev"]
        # Taking care of the tracking button toggle.
        if event.button == 1:  
            # left click
            game_world_point = self.screenxy_to_relativexy(event.pos)
            
            #Define a rect that matches the actual area in the info display where the track toggle icon is.
            track_rect = pygame.Rect(self.width - 30, 0, 30, 30)
            
            if track_rect.collidepoint(game_world_point) == True:
                if self.track == True:
                    self.track = False
                else:
                    self.track = True
