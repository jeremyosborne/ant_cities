"""Team colors and icon colors, and maybe other colors.
"""

def entity_colors(entity):
    """Base colors for an entity, taking into account things like team.
    """
    # Default.
    color = (0, 0, 0)
    # Most to least likely.
    if entity.name == "ant" and entity.team == 1:
        color = (255, 0, 0)
    elif entity.name == "ant" and entity.team == 2:
        color = (0, 0, 255)
    elif entity.name == "leaf":
        color = (0, 255, 0)
    elif entity.name == "base" and entity.team == 1:
        color = (255, 80, 80)
    elif entity.name == "base" and entity.team == 2:
        color = (80, 80, 255)
    
    return color
