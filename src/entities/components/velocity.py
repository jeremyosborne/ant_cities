from entities.components.component import Component
from common.calc import mmval, Heading, courseto
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
        self.speed = speed
        self.course = Heading(course)

        self.acceleration = acceleration
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
    
        # {float|None}
        self.target_speed = None
        # {Heading|None}
        self.target_course = None

    @property
    def speed(self):
        """ {float} Magnitude of our course.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = abs(float(value))

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
    def deltaxy(self):
        """{tuple} A screen coordinate friendly (upper left is left, positive
        x is right, positive y is down) velocity vector in one unit time.
        """
        deltas = self._course.screenxy
        return (deltas[0]*self.speed, deltas[1]*self.speed)

    def fullspeedto(self, locimp_or_course):
        """Aims target velocity toward an entity or along a course.
        
        locimp_or_course {mixed} Either an object that implements the location
        interface defined in this game, or a generic heading object representing
        course (numbers are okay, they are converted to Headings).
        """
        self.target_speed = self.max_speed
        if (hasattr(locimp_or_course, "location")):
            self.target_course = courseto(self.entity.location, locimp_or_course.location)
        else:
            self.target_course = locimp_or_course
    
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
            angleto = self.course.angleto(self.target_course)
            direction = -1 if angleto <= 0 else 1
            delta = direction * time_passed * self.rotation_speed
            if abs(delta) <= abs(angleto):
                self.course += delta
            else:
                self.course = self.target_course
                
        loc = self.entity.location
        dx, dy = self.deltaxy
        self.entity.location = loc[0]+dx*time_passed, loc[1]+dy*time_passed
