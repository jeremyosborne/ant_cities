import sys
import os
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),"../src")))

import pygame
from pygame.locals import *

import viewport

class Mini_Map(viewport.Viewport):
    def __init__(self, x_right=0, y_down=0, width=256, height=256, world_width=1024, world_height=768):
        viewport.Viewport.__init__(self, x_right, y_down, width, height, 1, 0, True)

def run():
    
    pygame.init()
    screen = pygame.display.set_mode((1000, 600), 0, 32)    

    game_screen = viewport.Viewport(0, 0, 1000, 600, 1, 0, True)
    print sys.getrefcount(game_screen)
    
    box1 = viewport.Viewport(100, 100, 256, 128, 1, 1, True)
    mini_map = Mini_Map()
    
    mini_map.is_visable = True
    
    print mini_map.is_visable
    print sys.getrefcount(mini_map)
    mini_map.delete()
    
    print mini_map.is_visable
    print sys.getrefcount(mini_map)


if __name__ == "__main__":
    
    run()
    exit()