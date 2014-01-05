import math
import time

from pymunk.vec2d import Vec2d

from entities.components import get_component
from entities.ai.brains import Brain


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
        
        # Components are stored for easy iteration...
        self._components_list = []
        # ...and made available to the public via an index of named components.
        self.components = {}
        
        # Movement in the game world
        self.location = (0., 0.)
        self.destination = (0., 0.)
        
        # A flag flipped when this entity has been deleted. For lazy cleanup.
        self.deleted = False
        
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        self._location = Vec2d(value)
        
        self.world.spatial_index.update(self)
    
    @property
    def destination(self):
        return self._destination
    
    @destination.setter
    def destination(self, value):
        self._destination = Vec2d(value)
        
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
    
    def add_component(self, cname, **kwargs):
        """Interface to adding a component to an entity.
        
        cname {str} Name of the component to add.
        kwargs {kwargs} Labeled arguments to pass in to the instantiation
        of the component.
        """
        # Load and immediately instantiate.
        component = get_component(cname)(**kwargs)
        # Part of the contract: we must add ourselves as an entity reference.
        component.entity = self
        # Add for easy iteration as well as easy reference.
        self._components_list.append(component)
        self.components[component._cname] = component
    
    def remove_component(self, name):
        """Remove a particular component from the component hash.
        
        name {str} Name of the component to remove.
        """
        # Remove index and location in list. This should be an uncommon operation.
        component = self.components.pop(name)
        self._components_list.remove(component)
        # Part of the contract: call destroy on the component.
        component.destroy()

    def process(self, time_passed):
        """Update this entity.
        
        time_passed {float} how much time has passed since the last call in 
        seconds.
        """
        # AI.
        self.brain.process(time_passed)

        # Update components.
        for component in self._components_list:
            component.process(time_passed)
    
    def delete(self):
        """Called during the end of life removal of an entity from the world.
        
        Intended to be augmented in subclasses, please call the super when
        overriding.
        """
        self.deleted = True
