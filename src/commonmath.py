"""Math functions that I can't find anywhere else.

Please replace these functions with already written ones,
or let me know if others exist in our libraries if I can't
find them.
"""

import math
from random import random, randint



MOD_360 = 360.
PI2 = math.pi*2
PIDIV2 = math.pi/2



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



def mmval(mx, val, mn=0):
    """Return the value if within maxi or mini, otherwise return the boundary
    (mini if less than mini, maxi if greater than maxi).
    
    mx {number} Upper bound.
    val {number} Value to boundary check.
    [mn=0] {number} Lower bound, assumes zero.
    
    return {number} val or associated boundary.
    """
    return max(mn, min(val, mx))



class Heading(object):
    """Handle facing/direction calculations.
    
    Using degrees: 0 is facing north, 90 is east, 180 is south, 270 is west.
    
    Using radians: 0 is north, pi/2 is east, pi is south, 3*pi/2 is west.
    """
    def __init__(self, current=0.):
        """Constructor.
        
        facing {float} The initial facing of our entity.
        """
        self.current = current

    def __add__(self, other):
        return Heading(self.current + other)

    __radd__ = __add__

    def __iadd__(self, other):
        self.current += other
        return self

    def __sub__(self, other):
        return Heading(self.current - other)

    __rsub__ = __sub__
    
    def __isub__(self, other):
        self.current -= other
        return self

    @property
    def current(self):
        """ {float} heading in degrees.
        """
        return self._current

    @current.setter
    def current(self, value):
        """ {number} set in degrees.
        """
        # This will work for positive or negative numbers, where the 
        # negative numbers are "corrected" via modulo. 
        # It's a factor of 10 faster than the more logical math.fmod().
        self._current = value % MOD_360

    @property
    def current_rad(self):
        """ {float} Current heading as radians.
        """
        return math.radians(self._current)
    
    @current_rad.setter
    def current_rad(self, value):
        """ {float}
        """
        # math.degrees is about 45% faster than arithmetic conversion.
        self._current = math.degrees(value) % MOD_360
    
    @property
    def cartesian_rad(self):
        """ {float} Convert a heading into cartesian radians 
        (heading 90 deg == cartesian 0 deg).
    
        Useful when passing the heading to trig functions.
        """
        return PI2 - math.radians(self.current) + PIDIV2

    @property
    def screenxy(self):
        """Return the deltas x,y that make up the unit circle x,y for this
        heading.
        
        Function is used to determine how much heading should be applied in the x
        direction and the y direction (e.g. for applying velocity over time to an
        entity's location).
        
        x,y units and signage are screen coordinates, with the following
        assumptions:
        
        positive x is right, negative x is left.
        
        positive y is down, negative y is up.
        
        return {tuple} The (x, y) components of this heading.
        """
        heading_rad = self.cartesian_rad
        signage = 1 if self.current <= 180 else -1 
        x = math.copysign(math.sqrt(1-math.sin(heading_rad)**2), signage)
        signage = 1 if self.current >= 90 and self.current <= 270 else -1
        y = math.copysign(math.sqrt(1-math.cos(heading_rad)**2), signage)
        return (x, y)
