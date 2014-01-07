import math
from entities.components.component import Component
from commonmath import mmval, Heading



class VelocityEngine(Component):
    """An optional component for managing Velocity via acceleration and
    angular rotation.
    
    Requires Entity have a Velocity component.
    """
    _cname = "velocityengine"
    
    def __init__(self, acceleration=0., max_speed=0., rotation_speed=0.):
        """Set initial values.
        
        acceleration {float} Velocity change applied per second.
        max_speed {float} Maximum speed per second.
        rotation_speed {float} How fast we can change course.
        """
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
    
        # {float|None}
        self.target_speed = None
        # {Heading|None}
        self.target_course = None
    
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
        if isinstance(value, Heading):
            self._target_course = value
        elif value is not None:
            self._target_course = Heading(value)
        else:
            self._target_course = None

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
        # Entity must have a velocity component.
        velocity = self.entity.components["velocity"]
        
        if self.target_speed != None and self.target_speed != velocity.speed:
            direction = 1 if self.target_speed > velocity.speed else -1
            delta = time_passed * self.acceleration
            speed = velocity.speed + math.copysign(delta, direction)
            velocity.speed = mmval(self.target_speed, speed)
        
        if self.target_course != None and self.target_course != velocity.course:
            direction = 1 if self.target_course > velocity.course else -1
            delta = time_passed * self.rotation_speed
            course = velocity.course + math.copysign(delta, direction)
            if (direction == 1 and course > self.target_course) or \
                (direction == -1 and course < self.target_course):
                velocity.course.set(self.target_course)
            else:
                velocity.course = course

            
        
