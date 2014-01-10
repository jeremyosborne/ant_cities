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

    def __init__(self, world):

        #a way for an entity to get at attributes about the world.
        self.world = world
        
        self.brain = Brain(self)
        
        # Entity promises to have a unique id.
        self.id = world.generate_id()
        
        # Component interface.
        self.c = Components(self)
        
        # Where we are currently located.
        self._location = Vec2d(0, 0)
        
        # A flag flipped when this entity has been deleted. For lazy cleanup.
        self.deleted = False
        
    @property
    def location(self):
        """{Vec2d} Where the entity is currently located.
        """
        return self._location
    
    @location.setter
    def location(self, value):
        """{Vec2d}
        """
        # We assume that location 
        self._location.x = value[0]
        self._location.y = value[1]
        
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
        self.deleted = True
