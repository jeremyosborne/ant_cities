from entities.components.component import Component
from common.calc import mmval



class Attribute(object):
    """Represents a single attribute.
    """
    def __init__(self, name, val, mx=None, mn=0):
        # What is the name of this attribute?
        self.name = name
        # What is the maximum value of the attribute.
        self.max = mx or val
        # What is the minimum value of the attribute.
        self.min = mn
        # What is the current value of the attribute.
        self.val = val

    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, value):
        self._val = mmval(self.max, value, self.min)



class Attrs(Component):
    """Used to track simple and numeric attributes on an entity.
    """
    
    _cname = "attrs"
    
    doprocess = False
    
    def __init__(self):
        # Cache of attributes.
        self.attributes = {}
    
    def __contains__(self, name):
        # Pass through to the underlying dict.
        return name in self.attributes
        
    def __getitem__(self, name):
        # If someone is attempting to get an attribute from the outside world,
        # we assume they want the value.
        return self.attributes[name].val
    
    def __setitem__(self, name, value):
        # Constrain value settings to the constraints supplied within the
        # attribute instance.
        self.attributes[name].val = value
    
    def get(self, name):
        """Get the underlying Attribute object.
        """
        return self.attributes[name]
    
    def create(self, name, val, mx=None, mn=0):
        """Create a new managed attribute.
        """
        self.attributes[name] = Attribute(name, val, mx, mn)
    
    def delta(self, name, diff):
        """Attempt to incrementally change an attribute by a particular value.
        
        return the actual change applied by the constraints of the attribute.
        """
        original_val = self.attributes[name].val
        self.attributes[name].val += diff
        
        if original_val + diff == self.attributes[name].val:
            return diff
        else:
            return self.attributes[name].val - original_val

        