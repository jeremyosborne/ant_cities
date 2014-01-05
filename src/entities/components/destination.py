from entities.components.component import Component
from entities.entity import Entity
from commonmath import Heading, courseto, distanceto
import math

class Destination(Component):
    """Handles various destination types for an entity and makes sure things
    like distanceto, courseto, location, etc. are available.
    
    When tracking entities, remember that entities can cease to exist
    at any time and care will need to be taken not to assume that tick to tick
    the entity is still there.
    """
    
    _cname = "destination"
    
    def __init__(self, val=None):
        """Constructor.
        
        Valid destinations are Entity derived instances and (x,y) coordinates.
        """
        self.val = val

    @property
    def val(self):
        """{Entity|Point|None} Destinations can be entities, objects acting
        as (x,y) coordinates, or None.
        """
        if self.isentity or self.ispoint:
            return self._val
        else:
            # Undo invalid settings.
            self._val = None
            return self._val
    
    @val.setter
    def val(self, val):
        # Allow the getter to do the cleanup, since it will be called more
        # and things can change after setting.
        self._val = val

    @property
    def location(self):
        """Location coordinates (x,y) of where we are headed.
        """
        if isinstance(self.val, Entity):
            return self.val.location
        else:
            # Assume that we have a location.
            return self.val

    @property
    def courseto(self):
        """{Heading|None} Straight line heading to destination.
        """
        if isinstance(self.val, Entity):
            return Heading(courseto(self.entity.location, self.val.location))
        elif self.ispoint:
            return Heading(courseto(self.entity.location, self.val))
        else:
            return None

    @property
    def distanceto(self):
        """{float|None} Straight line distance to destination.
        """
        if self.isentity:
            return distanceto(self.entity.location, self.val.location)
        elif self.ispoint:
            return distanceto(self.entity.location, self.val)
        else:
            return None

    @property
    def isentity(self):
        """{bool} Is the destination a valid entity?
        """
        if isinstance(self.val, Entity) and self.inworld:
            return True
        else:
            return False
    
    @property
    def ispoint(self):
        """{bool} Is the destination a point and not an entity.
        
        Does not confirm the validity of the point.
        """
        p = self.val
        if hasattr(p, "__getitem__") and (p[0] is not None) and (p[1] is not None):
            return True
        else:
            return False
    
    @property
    def isvalid(self):
        """{bool} Do we have a valid destination?
        
        Valid is a bit simple at the moment and there are not rigorous checks 
        in place.
        """
        return self.ispoint or self.isentity
    
    def set(self, val):
        """Convenience for setting the value of the destination.
        """
        self.val = val

    def clear(self):
        """Unset the destination even if the destination is still valid.
        """
        self.val = None
