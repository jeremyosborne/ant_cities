import math
from entities.components.component import Component
from commonmath import mmval

MOD_DEG = 360.0

class VelocityEngine(Component):
    """An optional component for managing Velocity via acceleration and
    angular rotation.
    
    Requires Entity have a Velocity component.
    """
    _cname = "velocityengine"
    
    # Attributes to treat as floats.
    _floaters = {"acceleration", 
                 "max_speed", 
                 "rotation_speed",
                 "target_speed", 
                 "target_course"
                 }
    
    def __init__(self, acceleration=0., max_speed=0., rotation_speed=0.):
        """Set initial values.
        
        acceleration {float} Velocity change applied per second.
        max_speed {float} Maximum speed per second.
        rotation_speed {float} How fast we can change course.
        """
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
    
        self.target_speed = None
        self.target_course = None
        
    def __setattr__(self, name, value):
        """Manage types.
        """
        if name in self._floaters and value != None:
            self.__dict__[name] = float(value)
        else:
            super(VelocityEngine, self).__setattr__(name, value)
    
    def update(self, speed=None, course=None):
        """Set a new speed and course target.
        
        speed {float} New speed.
        course {float} New course (in degrees).
        """
        self.target_speed = float(mmval(speed, self.max_speed))
        self.target_course = float(course) % MOD_DEG
        
    def coast(self):
        """Stop modifying speed and course.
        """
        self.target_speed = None
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
            velocity.speed = mmval(speed, self.target_speed)
        
        if self.target_course != None and self.target_course != velocity.course:
            direction = 1 if self.target_course > velocity.course else -1
            delta = time_passed * self.rotation_speed
            course = velocity.course + math.copysign(delta, direction)
            velocity.course = course
            if direction == 1 and course > self.target_course or \
                direction == -1 and course < self.target_course:
                velocity.course = self.target_course
            
        
