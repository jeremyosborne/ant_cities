import os
import pygame
import globaldata

from ui.assets.assets import AssetCache



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



class GameAssets(object):
    """Intended to be a unified asset loader.
    """
    def __init__(self, asset_path):
        self.image_assets = ImageAssets(asset_path)
        
    
    #-------------------------------------------------------------------------
    # Color used if label doesn't exist.
    default_color = (0, 0, 0)
    
    # Naming scheme is made up of entity duck typed name and the team id.
    colors = {
        # Entity specific colors.
        "ant-1": (0, 0, 255),
        "ant-2": (255, 0, 0),
        "anthill-1": (170, 170, 255),
        "anthill-2": (255, 170, 170),
        "leaf": (0, 255, 0),
        
        # General entity rendering colors.
        "empty_bar": (255, 0, 0),
        "energy_bar": (230, 100, 230),
        "health_bar": (0, 255, 0),
    }
    
    def color(self, thing):
        """Colors for an entity, taking into account things like team.
        """
        if hasattr(thing, "isentity") and thing.team_id:
            # Prefer entities with team ids.
            key = "%s-%s" % (thing.name, thing.team_id)
        elif hasattr(thing, "name"):
            # Prefer just entity names.
            key = thing.name
        else:
            # Allow for just strings, too.
            key = thing
        
        return self.colors.get(key, self.default_color)

    #-------------------------------------------------------------------------
    # Default image used if the image name doesn't exist.
    default_image = "_default"
    
    def image(self, thing):
        """Image for an entity, taking into account things like team.
        """
        if hasattr(thing, "isentity") and thing.team_id:
            # Prefer entities with team ids.
            key = "%s-%s" % (thing.name, thing.team_id)
        elif hasattr(thing, "name"):
            # Prefer just entity names.
            key = thing.name
        else:
            # Allow for just strings, too.
            key = thing
        
        try:
            return self.image_assets.get(key)
        except Exception:
            # If we blow it here, then we should explode.
            return self.image_assets.get(self.default_image)
