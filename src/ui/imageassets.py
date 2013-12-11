import os
import pygame

from ui.assets import AssetCache

class ImageAssets(AssetCache):
    """Implement asset cache for images used by Ant Cities.
    """
    def __init__(self, basepath):
        super(ImageAssets, self).__init__(basepath)
    
    def _loader(self, path):
        """Assumes we're only loading pygame images.
        """
        return pygame.image.load(path).convert_alpha()
    
    def _copier(self, img):
        """Assumes we're getting a pygame surface.
        """
        return img.copy()
    
    def path_translator(self, name):
        """Override the asset requester to allow passing of simple tokens
        as asset names.
        """
        # Assume all are pngs.
        return "%s.%s" % (os.path.join(self.basepath, name), "png")

