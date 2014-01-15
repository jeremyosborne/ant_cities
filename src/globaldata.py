import os

# File locations.
# Base directory to the assets.
ASSETS_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "assets"))

# Strings
GAME_TITLE = "Ant Cities"

# Screen Based (width, height)
SCREEN_SIZE = (1200, 700)

# World Based (width, height)
WORLD_SIZE = (1200*6, 530*6)

# Game settings.
ANT_COUNT = 60

NEST_POSITION = (256, WORLD_SIZE[1]/2)
NEST_POSITION_2 = (WORLD_SIZE[0] - 256, WORLD_SIZE[1]/2)

