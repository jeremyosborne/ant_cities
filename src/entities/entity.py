from pygame import Rect
from pymunk.vec2d import Vec2d

from entities.components import get_component
from entities.ai.brains import Brain



class Components(object):
    """Component collection and management.
    """
    def __init__(self, entity):
        # Components need to know who we are.
        self.entity = entity
        # Components are stored for easy iteration...
        self._list = []
        # ...and made available to the public via an index of named components.
        self._index = {}

    def __iter__(self):
        # list provides faster iteration than a dict.
        return self._list.__iter__()

    def __getitem__(self, key):
        # dict provides faster access than list.
        return self._index[key]

    def __contains__(self, key):
        return key in self._index

    def add(self, cname, **kwargs):
        """Interface to adding a component to an entity.
        
        cname {str} Name of the component to add.
        kwargs {kwargs} Labeled arguments to pass in to the instantiation
        of the component.
        """
        # Load and immediately instantiate.
        component = get_component(cname)(**kwargs)
        # Part of the contract: we must add ourselves as an entity reference.
        component.entity = self.entity
        # Add for easy iteration as well as easy reference.
        self._list.append(component)
        self._index[component._cname] = component
    
    def remove(self, name):
        """Remove a particular component from the component hash.
        
        name {str} Name of the component to remove.
        """
        # Remove index and location in list. This should be an uncommon operation.
        component = self._index.pop(name)
        self._list.remove(component)
        # Part of the contract: call destroy on the component.
        component.destroy()



class Entity(object):
    """Abstract base entity.
    """

    # Generic name for this entity. Subclass must set this class property or
    # override in constructor.
    name = "entity"
    
    # Width and height of the body of this entity. Used in collision tests.
    # Override in subclasses to change the size.
    body_size = 25

    # A simple flag to avoid the need for isinstance.
    isentity = True

    # Recognized official flags.
    # Flags can be used for experimental states while a more robust system
    # is developed.
    FLAGS = {
             # Entity should be garbage collected.
             "destroyed",
             # Entity is in play.
             "in world",
             # Entity is within an inventory and not part of the world.
             "in inventory",
             }

    def __init__(self, world):

        # Reference to world entity is in.
        self.world = world
        
        # Logic handled in the brain of an entity.
        self.brain = Brain(self)
        
        # Physical space taken up by this entity (always rectangle).
        # Treat as read only.
        self.body = Rect(0, 0, self.body_size, self.body_size)

        # Where we are currently located.
        self._location = Vec2d(0, 0)
        
        # Entity promises to have a unique id.
        self.id = world.generate_id()
        
        # Component interface.
        self.c = Components(self)
        
        # Flags indicating various states entity is in.
        self.flags = set()
        
    @property
    def location(self):
        """{Vec2d} Where the entity is currently located.
        """
        return self._location
    
    @location.setter
    def location(self, value):
        """{Vec2d}
        """
        # Move both body and location.
        # Rects don't like floats, only ints, so location is still valuable.
        self.body.centerx = self._location.x = value[0]
        self.body.centery = self._location.y = value[1]
        
        self.world.validate_entity_location(self)
            
    @property
    def team_id(self):
        """By default, we are neutral.
        """
        return None
    
    @property
    def inworld(self):
        """{bool} In play or have we been removed from the world.
        """
        if self.world and self.world.find(self.id) == self:
            return True
        else:
            return False
    
    def find_closest_entity(self, the_range=100., name=None):
        """Finds an entity closest to self within given range.
        
        the_range {number} Distance units radius to search within.
        [name] {str|set} A single or set of entity categories to filter
        against. (e.g. "leaf" or {"leaf", "ant"}).
        
        returns (closest_entity, distance), where closest_entity is an object
        reference and distance is the distance in pixels from the initial
        location.
        """
        if name is not None:
            # be nice to strings and sequences, even though we officially
            # only support sets.
            if type(name) == str:
                v = lambda e: e != self and e.name == name
            else:
                v = lambda e: e != self and e.name in name
        else:
            # default validation.
            v = lambda e: e != self

        return self.world.find_closest(self.location, the_range, v)
    
    def process(self, time_passed):
        """Update this entity.
        
        time_passed {float} how much time has passed since the last call in 
        seconds.
        """
        # AI.
        self.brain.process(time_passed)

        # Update components.
        for component in self.c:
            component.process(time_passed)
    
    def delete(self):
        """Called during the end of life removal of an entity from the world.
        
        Intended to be augmented in subclasses, please call the super when
        overriding.
        """
        self.flags.add("destroyed")
