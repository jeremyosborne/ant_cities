"""Team colors and icon colors, and maybe other colors.
"""

# Color used if label doesn't exist.
default_color = (0, 0, 0)

# Naming scheme is made up of entity duck typed name and the team id.
colors = {
    "ant-1": (0, 0, 255),
    "ant-2": (255, 0, 0),
    "anthill-1": (170, 170, 255),
    "anthill-2": (255, 170, 170),
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
