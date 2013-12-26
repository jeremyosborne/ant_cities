import pygame
import ui.viewport as viewport

class ViewUnitInfoBox(viewport.Viewport):
    """Traditional area that displays information about a single unit a user has clicked on.
    """
    def __init__(self, x_right=0, y_down=0, width=256, height=256, 
                 controller=None, imageassets=None):
        """Arguments not inherited from viewport.
        
        controller {EventPublisher} Provides a pipeline to events in the outside
        world.
        imageassets {AssetCache} Image cache.
        """

        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 1, True)

        self.font = pygame.font.SysFont("arial", 16)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))

        # Add title to the background image.
        label = self.font.render("Unit Info", True, (255, 255, 255))
        w, _ = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        pygame.draw.line(self.background, (255, 255, 255), (0, 0), (0, self.height), 10)
        
        self.surface.blit(self.background, (0, 0))

        self.description = "Unit Info."
        
        #The unit we're watching.
        self.watching_entity = None
        # Image to show which leaf is being watched.
        #self.watched_leaf_image = imageassets.get("leaf2")
        #Toggle for tracking the entity on screen.
        self.track = False
        
        #Load Button Icons
        self.Start_Tracking_Button = imageassets.load("track-enable")
        self.Stop_Tracking_Button = imageassets.load("track-disable")
                
        # Register event listeners.
        if controller is not None:
            controller.sub("MOUSEBUTTONDOWN", self.mousebuttondown_listener)
        elif __debug__:
            print "WARNING: controller was not defined, no event listening will be happening in", self

    
    def set_unit(self, entity):
        self.watching_entity = entity
        
    def update(self, world_viewport):
        self.surface.blit(self.background, (0, 0))
        
        if not self.watching_entity:
            self.surface.blit(self.background, (0, 0))
            self.track = False
            return

        # else... cut down on indenting.
        ent = self.watching_entity
        
        if self.track == True:
            # Track the unit visually and show toggle off.
            world_viewport.move_viewport(*ent.location)
            self.surface.blit(self.Start_Tracking_Button, (self.width - 30, 0))            
        else:
            self.surface.blit(self.Stop_Tracking_Button, (self.width -30, 0))
            
        # Unit details.
        unit_text = self.font.render(ent.name, True, (255, 255, 255))
        w, _ = unit_text.get_size()
        self.surface.blit(unit_text, ((self.width / 2) - w / 2, 15))
        
        output = ["Location: (%d, %d)" % tuple(ent.location)]

        if self.watching_entity.name == "ant":
            output.append("Energy: %s" % ent.components["energy"].current)
            output.append("Health: %s" % ent.components["health"].current)
            output.append("Brain state: %s" % ent.brain.active_state.name)
            output.append("Speed: %d" % ent.speed)
            output.append("Destinaton: (%d, %d)" % tuple(ent.destination))
            output.append("Distance to destination: %d" % ent.location.get_distance(ent.destination))
            
            if ent.brain.active_state.name == "seeking":
                if ent.leaf_id != None:
                    leaf = ent.world.get(ent.leaf_id)
                    if leaf != None:
                        output.append("Location of leaf: (%d, %d)" % tuple(leaf.location))
            
        for i, line in enumerate(output):
            text = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text, (10, 30 + i*15))
        
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
