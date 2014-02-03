"""Code for rendering entity specific things.

With all the entities floating around, use this library while namespaced
or aliased.
"""

import pygame
import globaldata
from ui.assets.gameassets import GameAssets

# We'll keep our own copy here for now.
game_assets = GameAssets(globaldata.ASSETS_PATH)



def inventory(entity, surface):
    """Display entity carried inventory.
    
    This function is woefuly incomplete for a paper-doll system, and will
    need the hard coded assumptions reworked.
    
    Returns the surface with the inventory rendered as a convenience (inventory
    is written onto the provided surface.
    """
    if entity.c["inventory"].carried:
        # Only the first thing in the inventory right now.
        inventory_image = game_assets.image(entity.c["inventory"].carried[0])
        # Assume it is a leaf, so we rotate it to fit in the mouth.
        inventory_image = pygame.transform.rotate(inventory_image, -90)
        surface.blit(inventory_image, (surface.get_width()/2-inventory_image.get_width()/2, 0))
    return surface


def statusbars(entity, surface):
    """Display generic status bars for a particular entity attributes if
    the entity as the attributes.
    
    Pass the entity and the surface on which to render the status bars.
    Rendering is done at a "default" size, assumes scaling is performed
    after.
    
    Returns the surface with the status bars rendered as a convenience (status
    bars are written onto the provided surface.
    """
    # Quick exit if no attrs.
    if "attrs" not in entity.c:
        return surface
    
    # Common settings.
    width = 25
    height = 4
    # Initial offset.
    offsetx = 0
    offsety = 0
    empty_color = game_assets.color("empty_bar")
    bar = pygame.surface.Surface((width, height)).convert()
    
    # Which attributes should we chart, if they exist?
    attribute_candidates = ["energy", "health"]
                    # (current, full color) for each attribute
                    # overlaid the default empty color.
    comps_to_draw = [(entity.c["attrs"].get(a), game_assets.color(a+"_bar")) 
                     for a in attribute_candidates if a in entity.c["attrs"]]
    # Attributes drawn from the top down.
    for i, v in enumerate(comps_to_draw):
        component, full_color = v
        bar.fill(empty_color)
        bar.fill(full_color, (offsetx, offsety, component.val/float(component.max)*width, height))
        surface.blit(bar, (offsetx, offsety+height*i))
    return surface



def strategic_icon(entity):
    """Renders the entity as a strategic icon on the view surface.
    
    Pass in the entity we wish to render.
    
    returns a new, unscaled surface representing the strategic icon.
    """
    color = game_assets.color(entity)
    surface = pygame.Surface((10, 10)).convert()
    surface.fill(color)
    return surface
