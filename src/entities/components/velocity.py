from entities.components.component import Component
from commonmath import Heading
import math

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
        self._course = Heading(course)
        # Update cached x/y values.
        self._reset_xy()

    def _reset_xy(self):
        """Resets the xy values. Call when setting speed or course.
        """
        # We assume we have more reads than writes.
        deltas = self._course.screenxy
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
        return self._course.current

    @course.setter
    def course(self, value):
        """ {number} set in degrees.
        """
        self._course.current = value
        self._reset_xy()

    @property
    def course_rad(self):
        """ {float}
        """
        return self._course.current_rad
    
    @course_rad.setter
    def course_rad(self, value):
        """ {float}
        """
        self._course.current_rad = value
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
