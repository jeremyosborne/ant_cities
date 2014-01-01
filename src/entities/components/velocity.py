import math
from commonmath import heading_xy
from entities.components.component import Component

MOD_DEG = 360.0
pi2 = math.pi*2
pidiv2 = math.pi/2

class Velocity(Component):
    """The course of our entity: speed plus direction. May be distinct from
    heading (facing) of the entity.
    
    Using degrees: 0 is north, 90 is east, 180 is south, 270 is west.
    
    Using radians: 0 is north, pi/2 is east, pi is south, 3*pi/2 is west.
    
    Degrees is the default, radians are optional.
    
    Magnitude of velocity is assumed to be applied along a unit vector.
    """
    
    _cname = "velocity"
    
    def __init__(self, speed=0., course=0.):
        """Constructor.
        """
        # Set defaults so our caching of properties works.
        self._speed = speed
        self._course = course
        # Update cached x/y values.
        self._reset_xy()

    def _reset_xy(self):
        """Resets the xy values. Call when setting speed or course.
        """
        # Unit circle math applied with corrected signage.
        # We do this approach because we assume we have more reads than writes.
        deltas = heading_xy(self.course)
        self._x = deltas[0] * self.speed
        self._y = deltas[1] * self.speed

    @property
    def speed(self):
        """ {float} Magnitude of our course.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = abs(float(value))
        self._reset_xy()

    @property
    def course(self):
        """ {float} course in degrees.
        """
        return self._course

    @course.setter
    def course(self, value):
        """ {number} set in degrees.
        """
        # This will work for positive or negative numbers, where the 
        # negative numbers are "corrected" via modulo. 
        # It's a factor of 10 faster than the more logical math.fmod().
        self._course = value % MOD_DEG
        self._reset_xy()

    @property
    def course_rad(self):
        """ {float}
        """
        return math.radians(self._course)
    
    @course_rad.setter
    def course_rad(self, value):
        """ {float}
        """
        # math.degrees is about 45% faster than arithmetic conversion.
        self._course = math.degrees(value) % MOD_DEG
        self._reset_xy()

    @property
    def x(self):
        """The magnitude of velocity in the x direction.
        
        positive x is assumed right (east), negative is assumed west (left).
        """
        return self._x
    
    @property
    def y(self):
        """The magnitude of velocity in the y direction.
        
        positive y is assumed up (north), negative y is assumed south (down).
        """
        return self._y

    def process(self, time_passed):
        loc = self.entity.location
        self.entity.location = loc[0]+self.x*time_passed, loc[1]+self.y*time_passed
