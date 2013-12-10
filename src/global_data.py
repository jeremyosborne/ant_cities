import os

# File locations.
# Base directory to the assets.
ASSETS_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "assets"))


# Control settings.
render_world = True
render_minimap = True

# Game settings.
ANT_COUNT = 60
NEST_SIZE = 5.

#Screen Based
screen_size = (1200,700)
screen_size_x = 1200
screen_size_y = 700

#World Based
world_size_x = 1200*6
world_size_y = 530*6

NEST_POSITION = (world_size_x - 256, world_size_y / 2)
NEST_POSITION_2 = (256, world_size_y / 2)

