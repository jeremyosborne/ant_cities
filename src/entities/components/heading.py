from entities.components.component import Component
import math

MOD_DEG = 360.0

class Heading(Component):
    """Which direction our entity is facing.
    
    This is in regards to navigational heading where the nose of a ship or
    aircraft might not be facing in the vessels velocity direction.
    
    Using degrees: 0 is facing north, 90 is east, 180 is south, 270 is west.
    
    Using radians: 0 is north, pi/2 is east, pi is south, 3*pi/2 is west.
    
    Degrees is the default, radians are optional.
    """
    
    _cname = "facing"
    
    def __init__(self, current=0.):
        """Constructor.
        
        facing {float} The initial facing of our entity.
        """
        self.current = current

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
        # negative numbers are "corrected" via rotation some magic modulo op. 
        # Even though this feels black magicky, it's a factor of 10 faster 
        # than the more logical math.fmod().
        self._current = value % MOD_DEG

    @property
    def current_rad(self):
        """ {float}
        """
        return math.radians(self._current)
    
    @current_rad.setter
    def current_rad(self, value):
        """ {float}
        """
        # math.degrees is about 45% faster than arithmetic conversion. go figure.
        self._current = math.degrees(value) % MOD_DEG
