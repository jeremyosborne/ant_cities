import pygame
import viewport

from game import imageassets


class ViewUnitInfoBox(viewport.Viewport):
    """Traditional area that displays information about a single unit a user has clicked on.
    """
    def __init__(self, x_right=0, y_down=0, width=256, height=256, controller=None):
        """Arguments not inherited from viewport.
        
        controller {EventPublisher} Provides a pipeline to events in the outside
        world.
        """

        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 1, True)

        self.font = pygame.font.SysFont("arial", 16)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))

        #Add title to the background image.
        label = self.font.render("Unit Information Display", True, (255, 255, 255))
        w, h = label.get_size()
        self.background.blit(label, ((self.width / 2) - w / 2, 0))
        
        pygame.draw.line(self.background, (255, 255, 255), (0, 0), (0, self.height), 10)
        
        self.surface.blit(self.background, (0, 0))

        self.description = "Unit Info."
        
        #The unit we're watching.
        self.watching_entity = None
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
        
    def update(self, world):
        #Is there something selected?
        self.surface.blit(self.background, (0, 0))
        if self.watching_entity != None:
            
            #Should we be tracking the unit?  And what kind of button should we show (Track/Untrack)?
            if self.track == True:
                #Track the unit.
                x, y = self.watching_entity.location
                world.viewport.update_viewport_center(x, y)
                #Draw button to untrack.
                self.surface.blit(self.Start_Tracking_Button, (self.width - 30, 0))            
                
            else:
                #Draw button to track.
                self.surface.blit(self.Stop_Tracking_Button, (self.width -30, 0))
                
            text = self.font.render("Location: " + str("{:10.4f}".format(self.watching_entity.location[0])), True, (255, 255, 255))
            self.surface.blit(text, (10, 60))
            text = self.font.render(str("{:10.4f}".format(self.watching_entity.location[1])), True, (255, 255, 255))
            self.surface.blit(text, (150, 60))
            
            #Unit Type
            unit_text = self.font.render(self.watching_entity.name, True, (255, 255, 255))
            w, h = unit_text.get_size()
            self.surface.blit(unit_text, ((self.width / 2) - w / 2, 15))
            if self.watching_entity.name == "ant":
                text = self.font.render("State: " + self.watching_entity.brain.active_state.name, True, (255, 255, 255))
                self.surface.blit(text, (10, 30))
                
                text = self.font.render("Speed: " + str(self.watching_entity.speed), True, (255, 255, 255))
                self.surface.blit(text, (138, 30))
            
                text = self.font.render("Destinaton: " + str(self.watching_entity.destination), True, (255, 255, 255))
                self.surface.blit(text, (10, 45))
                
                text = self.font.render("Distance to Destinaton: " + str("{:10.4f}".format(self.watching_entity.location.get_distance(self.watching_entity.destination))), True, (255, 255, 255))
                self.surface.blit(text, (10, 75))
                
                if self.watching_entity.brain.active_state.name == "seeking":
                    if self.watching_entity.leaf_id != None:
                        #change the leaf image.
                        leaf = self.watching_entity.world.get(self.watching_entity.leaf_id)
                        if leaf != None:
                            leaf.image = self.watching_entity.world.leaf_image2
                            #Put more on the screen about this leaf.
                            text = self.font.render("Location of leaf: " + str(leaf.location), True, (255, 255, 255))
                            w, h = text.get_size()
                            self.surface.blit(text, (10, 90))
                        
                
        else:
            self.surface.blit(self.background, (0, 0))
            self.track = False
        
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
