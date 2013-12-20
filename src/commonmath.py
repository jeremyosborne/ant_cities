"""Math functions that I can't find anywhere else.

Please replace these functions with already written ones,
or let me know if others exist in our libraries if I can't
find them.
"""

from math import sqrt
from random import random, randint

def random_sign():
    """Generate either +1 or -1.
    """
    return -1 if random() >= 0.5 else 1

def random_radial_offset(max_length):
    """Generate a random offset from a point (origin assumed to be (0, 0)).
    As number of function calls -> infinity, random offsets will form a
    cloud in the shape of a circle around the origin.
    
    max_length {int} Maximum radial distance offset.
    
    returns {tuple} of ({int} x, {int} y) as a random offset.
    """
    x = randint(0, max_length)
    ymax = int(sqrt(max_length**2 - x**2))
    y = randint(0, ymax)
    return (random_sign()*x, random_sign()*y)

def random_boxed_offset(max_length):
    """Generate a random offset from a point (origin assumed to be (0, 0)).
    As number of function calls -> infinity, random offsets will form a
    cloud in the shape of a box around the origin point.
    
    max_length {int} Maximum distance offset for the x distance and the y
    distance.
    
    returns {tuple} of ({int} x, {int} y) as a random offset.
    """
    # Randomize starting position.
    return (random_sign()*randint(0, max_length), random_sign()*randint(0, max_length))
