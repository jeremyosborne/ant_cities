"""Team colors and icon colors, and maybe other colors.
"""

# Color used if label doesn't exist.
default_color = (0, 0, 0)

# Naming scheme is made up of entity duck typed name and the team id.
colors = {
    "ant-1": (255, 0, 0),
    "ant-2": (0, 0, 255),
    "base-1": (255, 170, 170),
    "base-2": (170, 170, 255),
    "leaf": (0, 255, 0)
}

def entity_colors(entity):
    """Colors for an entity, taking into account things like team.
    """
    if entity.team_id:
        key = "%s-%s" % (entity.name, entity.team_id)
    else:
        key = entity.name
    
    return colors.get(key, default_color)
