"""Math functions that I can't find anywhere else.

Please replace these functions with already written ones,
or let me know if others exist in our libraries if I can't
find them.
"""

import math
from random import random, randint

pi2 = math.pi*2
pidiv2 = math.pi/2

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
    ymax = int(math.sqrt(max_length**2 - x**2))
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

def fdiv(a, b):
    """Divide and always return as a float.
    
    a {number} Dividend.
    b {number} Divisor.
    
    return {float} quotient as a float (e.g. .25)
    """
    return a/float(b)

def percint(a, b):
    """Calculate a percent.
    
    a {number} Dividend.
    b {number} Divisor.
    
    return {int} quotient as a truncated percent value (e.g. 25 for .25)
    """
    return int((a/float(b)) * 100)

def percfloat(a, b, ndigits=0):
    """Calculate a percent.
    
    a {number} Dividend.
    b {number} Divisor.
    [ndigits] {int} Number of digits to round to. Default is 0.
    
    return {float} quotient as a rounded percent value (e.g. 25.1 for .251)
    """
    return int(round((a/float(b) * 100), ndigits))

def mmval(val, maxi, mini=0):
    """Return the value if within maxi or mini, otherwise return the boundary
    (mini if less than mini, maxi if greater than maxi).
    
    val {number} Value to boundary check.
    maxi {number} Upper bound.
    [mini=0] {number} Lower bound, assumes zero.
    
    return {number} val or associated boundary.
    """
    return max(mini, min(val, maxi))

def heading_xy(heading=0.):
    """Take a heading or course and return parts x, y of the heading as parts 
    of a unit circle.
    
    Heading measurement is north = 0, east = 90, south = 180, west = 270.
    
    Function is used to determine how much heading should be applied in the x
    direction and the y direction (e.g. for applying velocity over time to an
    entity's location).
    
    heading {number} Heading in degrees.
    
    return {tuple} The (x, y) components of this heading.
    
    """
    heading_rad = math.radians(heading)
    signage = 1 if heading <= 180 else -1 
    x = math.copysign(math.sqrt(1-math.sin(pi2 - heading_rad + pidiv2)**2), signage)
    signage = 1 if heading >= 90 and heading <= 270 else -1
    y = math.copysign(math.sqrt(1-math.cos(pi2 - heading_rad + pidiv2)**2), signage)
    return (x, y)
