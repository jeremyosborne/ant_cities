from entities.components.component import Component
import commonmath
import math

class Heading(commonmath.Heading, Component):
    """Which direction our entity is facing.
    
    This is in regards to navigational heading where the nose of a ship or
    aircraft might not be facing in the vessels velocity direction.
    
    Using degrees: 0 is facing north, 90 is east, 180 is south, 270 is west.
    
    Using radians: 0 is north, pi/2 is east, pi is south, 3*pi/2 is west.
    
    Degrees is the default, radians are optional.
    """
    
    _cname = "heading"
    
    # Everything else should be made available through the heading class.
