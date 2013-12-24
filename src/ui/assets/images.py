"""Entity images.
"""

import globaldata
# We are going to have our own imageassets cache (this is wasteful).
from ui.assets.imageassets import ImageAssets

entity_assets = ImageAssets(globaldata.ASSETS_PATH)

# Default image used if the image name doesn't exist.
default_image = "_default"

def entity_images(entity):
    """Image for an entity, taking into account things like team.
    """
    if entity.team_id:
        key = "%s-%s" % (entity.name, entity.team_id)
    else:
        key = entity.name
    
    try:
        return entity_assets.get(key)
    except Exception:
        # If we blow it here, then we should explode.
        return entity_assets.get(default_image)
