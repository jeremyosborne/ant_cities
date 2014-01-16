import pygame
from ui.pygameview import PygameView

class DataColumnDisplay(PygameView):
    """Generic data display.
    
    Simple display of data with headers on left and title as first row.
    Data is passed in as a list of tuples, first element of tuple is the
    row header (str), second element of tuple is a callable object (function)
    that can be called and will return a str that will be used to display
    the updated data.
    """
    def subclass_init(self, title="Data Column Display", data=None):
        self.font_family = "arial"
        self.font_size = 16
        self.font = pygame.font.SysFont(self.font_family, self.font_size)
        self.fgcolor = (255, 255, 255)
        self.bgcolor = (0, 0, 0)
        # Whitespace between edge of box and content (pixels).
        self.padding = {
                        #"top": 0,
                        #"right": 0,
                        # NOTE: Currently only one implemented.
                        "left": 10,
                        #"bottom": 0
                        }
        # Additional whitespace between columns (pixels).
        self.column_padding = 5
                
        # Displayed at the top of the panel.
        self.title = title
        # Dual column display. (header, dynamic-data-as-callable)
        self.data = data or []
        # Used to align data displayed.
        self.max_data_label_width = 0

        self.background = pygame.surface.Surface((self.width, self.height)).convert()
        self.init_background()
                
    def init_background(self):
        self.background.fill(self.bgcolor)

        # Title.
        title_surface = self.font.render(self.title, True, self.fgcolor)
        w, _ = title_surface.get_size()
        self.background.blit(title_surface, (self.width/2 - w/2, 0))
        
        # Static info labels and determine width of label.
        for i, labeled_data in enumerate(self.data):
            data_label = self.font.render(labeled_data[0], True, self.fgcolor)
            # Save dynamic offset to align data against.
            self.max_data_label_width = max(data_label.get_size()[0]+self.padding["left"], self.max_data_label_width)
            self.background.blit(data_label, (self.padding["left"], self.font.get_linesize()*(1+i)))

    def clear(self):
        # Erase previous display with static surface.
        self.surface.blit(self.background, (0, 0))

    def draw(self, surface):
        # Update with dynamic data, defined by functions or callable objects.
        for i, labeled_data in enumerate(self.data):
            data = self.font.render(labeled_data[1](), True, self.fgcolor)
            self.surface.blit(data, (self.max_data_label_width+self.column_padding, self.font.get_linesize()*(1+i)))

        # Blit to the main surface.
        surface.blit(self.surface, ((self.x, self.y)))

