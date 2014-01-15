'''
Created on Jun 19, 2013

@author: john
'''

from random import randint
from commonmath import random_radial_offset, mmval
from entities.anthill import Anthill
from entities.leaf import Leaf
from entities.dummy import Dummy
import globaldata
import spatialengine



def gen_id():
    """Return a unique id for entities.
    """
    gen_id._next_id += 1
    return gen_id._next_id

gen_id._next_id = 0L



class World(object):
        
    def __init__(self, width, height):
        # The size of the world.
        self.width = width
        self.height = height

        self.spatial_index = spatialengine.SpatialEngine(self.width, self.height)
        
        # Dictionary of all the entities.
        self.entities = {}

        # The age of the world (real seconds of game time passed).
        self.age = 0
        
        #-----------------------------------------------------------------------
        # Setting up initial entities.
        #-----------------------------------------------------------------------

#         if __debug__:
#             # Dummy entity for testing components.
#             dummy = Dummy(self)
#             dummy.location = (self.width/2, self.height/2)
#             self.add_entity(dummy)

        # Generate bases.
        self.anthill_1 = Anthill(self, 1, "Blue Ants")
        self.anthill_1.location = globaldata.ANTHILL_POSITION
        self.add_entity(self.anthill_1)
        
        self.anthill_2 = Anthill(self, 2, "Red Ants")
        self.anthill_2.location = globaldata.ANTHILL_POSITION_2
        self.add_entity(self.anthill_2)

        # Generate ants.
        for _ in xrange(globaldata.ANT_COUNT):
            # Randomize starting position.
            startxy = random_radial_offset(100)
            # Red team (Team 1)
            ant = self.anthill_1.create_entity("ant", startxy)
            self.add_entity(ant)
            # Blue team (Team 2)
            ant = self.anthill_2.create_entity("ant", startxy)
            self.add_entity(ant)
        
    def add_entity(self, entity):
        """Place the entity in the world and into the update cycle.

        entity {Entity} An entity derived instance.
        """
        self.entities[entity.id] = entity
        
        # Update state.
        entity.flags.add("in world")

    def remove_entity(self, entity):
        """Remove an entity from the world and from the update cycle but
        do not mark the entity for deletion.
        
        entity {Entity} An entity derived instance.
        """
        del self.entities[entity.id]
        self.spatial_index.remove(entity)
        entity.flags.discard("in world")

    def destroy_entity(self, entity):
        """Remove an entity from the world, from the update cycle, and mark
        for deletion.
        
        If the entity has already been removed from the world, or was never
        placed within the world, the entity can just be destroyed.
        
        entity {Entity} An entity derived instance.
        """
        self.remove_entity(entity)
        entity.destroy()

    def validate_entity_location(self, entity):
        """Entities should call when they change their own location.
        
        Has a side effect of correcting entity locations at the boundaries,
        something entities shouldn't have to know about, as well as updating
        spatial indexes (something entities also shouldn't have to know about).
        
        This is experimental. This makes me want to rethink how objects are
        managed in the world and how movement occurs.
        
        entity {Entity} An entity with a location.
        """
        # Operate to speed up the writing.
        entity.location[0] = mmval(self.width, entity.location[0])
        entity.location[1] = mmval(self.height, entity.location[1])
        
        self.spatial_index.update(entity)

    def generate_id(self):
        """Returns an identifier unique in this world.
        
        Assumed usage with entities of this world.
        """
        return gen_id()
    
    def find(self, entity_id):
        """Retrieve an entity by id.
        
        entity_id {mixed} A value representing an entity id.
        
        returns {Entity|None} Returns a reference to the entity matched by
        id, or None if no entity was found.
        """
        return self.entities.get(entity_id)

    def find_closest(self, location, the_range=100., validation=None):
        """Find the closest entity to a point.
        
        In the event that there might be more than one entity that
        meets the closest criteria, this function will still return only one.
        
        location {tuple} A point object that expresses x,y world coordinates
        as items 0,1.
        [the_range] {number} Number of pixels from a location to search for
        an entity. Value is constrained by default.
        [validation] {function} A validation function that is used to filter()
        the entities found. The validation function will be passed a single
        argument which is a closest entity candidate. The function should return
        True if the entity is a valid choice, false if not. 
        
        returns (closest_entity, distance), where closest_entity is an object
        reference and distance is the distance in pixels from the initial
        location.
        """
        return self.spatial_index.find_closest(location, the_range, validation)
    
    def find_all_in_range(self, location, the_range=100., validation=None):
        """Returns list of all entities in range.

        location {tuple} A point object that expresses x,y world coordinates
        as items 0,1.
        [the_range] {number} Number of pixels from a location to search for
        an entity. Value is constrained by default.
        [validation] {function} A validation function that is used to filter()
        the entities found. The validation function will be passed a single
        argument which is a closest entity candidate. The function should return
        True if the entity is a valid choice, false if not. 

        return {Entity[]} any entities in range, or an empty list.
        """
        return self.spatial_index.find_all_in_range(location, the_range, validation)
    
    def process(self, time_passed):
        """Update the world.
        
        time_passed {float} ms since the last time this function was called.
        """
        # The entities work in seconds.
        time_passed_seconds = time_passed / 1000.0
        
        # Increase game time passed.
        self.age += time_passed_seconds
        
        # Here's our chance to throw in a new leaf.
        if randint(1, 20) == 1:
            leaf = Leaf(self)
            leaf.location = (randint(0, leaf.world.width), randint(0, leaf.world.height))
            self.add_entity(leaf)
        
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            if "dead" in entity.flags:
                self.destroy_entity(entity)
    