from entities.components.component import Component
from commonmath import mmval, Heading
import math

class Velocity(Component):
    """Provides motion for entity, along with some basic velocity helpers.
    """
    
    _cname = "velocity"
    
    def __init__(self, speed=0., course=0., acceleration=0., max_speed=0., rotation_speed=0.):
        """Constructor.

        speed {float} Initial speed.
        course {float} Initial course.
        acceleration {float} Max velocity change per second.
        max_speed {float} Maximum speed per second.
        rotation_speed {float} Max degrees rotation change per second.
        """
        # Set defaults so our caching of properties works.
        self._speed = speed
        self._course = Heading(course)
        # Update cached x/y values.
        self._reset_xy()

        self.acceleration = acceleration
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
    
        # {float|None}
        self.target_speed = None
        # {Heading|None}
        self.target_course = None

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
        return self._course

    @course.setter
    def course(self, value):
        """ {number} set in degrees.
        """
        self._course = Heading(value)
        self._reset_xy()

    @property
    def acceleration(self):
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = float(value)
    
    @property
    def max_speed(self):
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = float(value)
        
    @property
    def rotation_speed(self):
        return self._rotation_speed
    
    @rotation_speed.setter
    def rotation_speed(self, value):
        self._rotation_speed = float(value)
    
    @property
    def target_speed(self):
        return self._target_speed
    
    @target_speed.setter
    def target_speed(self, value):
        self._target_speed = mmval(self.max_speed, float(value)) if value is not None else None

    @property
    def target_course(self):
        return self._target_course
    
    @target_course.setter
    def target_course(self, value):
        if value is not None:
            self._target_course = Heading(value)
        else:
            self._target_course = None

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

    def update(self, speed=None, course=None):
        """Set a new speed and course target.
        
        speed {float} New speed.
        course {float} New course (in degrees).
        """
        self.target_speed = speed
        self.target_course = course

    def fullspeedto(self, course):
        self.target_speed = self.max_speed
        self.target_course = course
        
    def coast(self):
        """Stop modifying speed and course.
        """
        self.target_speed = None
        self.target_course = None
    
    def stop(self):
        """Keep same course, bring speed to 0.
        """
        self.target_speed = 0.
        self.target_course = None
    
    def process(self, time_passed):
        """Manage velocity.
        """
        if self.target_speed != None and self.target_speed != self.speed:
            direction = 1 if self.target_speed > self.speed else -1
            delta = time_passed * self.acceleration
            speed = self.speed + math.copysign(delta, direction)
            self.speed = mmval(self.target_speed, speed)
        
        if self.target_course != None and self.target_course != self.course:
            direction = 1 if self.target_course > self.course else -1
            delta = time_passed * self.rotation_speed
            course = self.course + math.copysign(delta, direction)
            if (direction == 1 and course > self.target_course) or \
                (direction == -1 and course < self.target_course):
                self.course.set(self.target_course)
                # Force a reset.
                self._reset_xy()
            else:
                self.course = course
                
        loc = self.entity.location
        self.entity.location = loc[0]+self.x*time_passed, loc[1]+self.y*time_passed
