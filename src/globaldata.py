import os

# File locations.
# Base directory to the assets.
ASSETS_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "assets"))

# Strings
GAME_TITLE = "Ant Cities"

# Game settings.
ANT_COUNT = 60
NEST_SIZE = 5.

# Screen Based (width, height)
SCREEN_SIZE = (1200, 700)

# World Based (width, height)
WORLD_SIZE = (1200*6, 530*6)

NEST_POSITION = (WORLD_SIZE[0] - 256, WORLD_SIZE[1]/2)
NEST_POSITION_2 = (256, WORLD_SIZE[1]/2)

# Control settings.
render_world = True
render_minimap = True
