'''
Created on Oct 20, 2013

@author: john
'''

from collections import deque



class SpatialEngine(object):
    ''' Coarser spatial storage for entities using 2d points for location.
    '''
    def __init__(self, world_size_x, world_size_y):
        '''
        Constructor
        
        world_size_x {int} number of pixels wide the world is.
        world_size_y {int} number of pixels hight he world is.
        '''
        #Size for X and Y for a grid element (cell.)
        self.cell_size = 100
        
        #Create the dictionary.
        self.spatial_index = {}
        # key == entity.id, value = cell containing entity
        self.entity_index = {}
        
        #Initialize the dictionary and create the empty lists.
        #It's possible for a unit to go over the edge of the world when turning, so there is
        #padding cells, hence the -1 and +2 below.
        for i in range (-1, world_size_x / 100+2):
            for j in range (-1, world_size_y / 100+2):
                self.spatial_index[i,j] = []

    def _insert(self, entity):
        """ Add an entity to the spatial index.
        Call update as the public API instead of _insert.
        
        entity {entity} Must provide a .id and .location interface to the 2d location
        of the entity.
        """
        # Prevention during dev.
        assert not self.entity_index.get(entity.id), "No double insertions."

        cell = self.which_cell(entity.location)
        self.spatial_index[cell].append(entity)
        # add lookup by id
        self.entity_index[entity.id] = cell
        
    def remove(self, entity):
        """ Remove an entity from the spatial index.
        
        entity {entity} Must provide a .id attribute uniquely identifying the
        entity.
        """
        if entity.id in self.entity_index:
            cell = self.entity_index[entity.id]
            self.spatial_index[cell].remove(entity)
            # delete lookup by id
            del self.entity_index[entity.id]
    
    def update(self, entity):
        """ Update an entity's location within the spatial index.
        
        entity {entity} Must provide a .id and .location interface to the 2d location
        of the entity.
        """
        self.remove(entity)
        self._insert(entity)

    def which_cell(self, point):
        '''Identifies which cell a coordinate belongs to.

        point {tuple} Unpackable 2d coordinate in the form of (x, y).
        
        return {tuple} Cell identifier.
        '''
        x = int(point[0] / self.cell_size)
        y = int(point[1] / self.cell_size)
        return (x, y)
    
    def which_cells_in_range(self, point, the_range):
        '''Given a point and a search radius, return the list of
        cells that should be considered.
        
        point {tuple} Unpackable 2d coordinate in the form of (x, y).
        the_range {number} How many pixels radius in which to search.
        
        return {list} List of identifiers in the form of.
        '''
        x, y = point
        #Determine the area we should be looking at.
        # TODO: If we pass too large a the_range in, limit to max size of grid.
        x1 = int((x + the_range) / self.cell_size)
        x2 = int((x - the_range) / self.cell_size)
        y1 = int((y + the_range) / self.cell_size)
        y2 = int((y - the_range) / self.cell_size)
        
        cell_list = []
        
        #Build the list of cells that match the area.
        for i in range(x2, x1):
            for j in range(y2, y1):
                if self.spatial_index.has_key((i,j)):
                    #Valid cell to search.
                    cell_list.append((i,j))
        return cell_list

    def find_all_in_range(self, point, the_range=1, validate=None):
        ''' Returns list of all entities in range.

        point {Vec2d} Location to search from.
        [tolerance=5.0] {float} Number of pixels radius to allow for a match.
        [validate] {function} If included, filters out possible results.

        return {deque} any entities in range, or an empty deque.
        '''
        cell_list = self.which_cells_in_range(point, the_range)
        # should timeit this... I think deques are faster than lists for how we
        # use them.
        entities = deque()
        for cell in cell_list:
            for entity in self.spatial_index[cell]:
                distance = entity.location.get_distance(point)
                if validate and not validate(entity):
                    # skip this entity
                    continue
                else:
                    entities.append((entity, distance))
        return entities

    def find_closest(self, point, the_range=1, validate=None):
        """ Find the closest entity.
        
        point {Vec2d} Where to search from.
        [the_range] {int} Number of pixels radius in which to search.
        [validate] {function} If included, filters out possible results.
        Behaves like the callback to the filter() builtin.
        
        return {tuple} containing (entity, distance) or (None, 0) if not found.
        """
        
        closest_entity = None
        closest_distance = the_range
        
        cell_list = self.which_cells_in_range(point, the_range)        
        for cell in cell_list:
            for entity in self.spatial_index[cell]: 
                distance = entity.location.get_distance(point)
                if distance <= closest_distance:
                    if validate and not validate(entity):
                        # skip this entity
                        continue
                    else:
                        closest_distance = distance
                        closest_entity = entity
        
        if not closest_entity:
            closest_distance = 0

        return (closest_entity, closest_distance)



if __name__ == "__main__":
    # Testing
    import global_data
    from random import randint
    from pymunk import Vec2d
    
    class MockLeaf(object):
        id = 0
        def __init__(self, location):
            MockLeaf.id += 1
            self.id = MockLeaf.id
            self.location = location
    
    spatial_index = SpatialEngine(global_data.world_size_x, global_data.world_size_y)
    leaf = MockLeaf(Vec2d(250, 350))
    leaf2 = MockLeaf(Vec2d(351, 451))
    
    spatial_index.update(leaf)
    spatial_index.update(leaf2)
    print "Contents of cell 2,3:"
    print (spatial_index.spatial_index[2, 3])
    
    closest = spatial_index.find_closest(leaf.location, 100,
                                         lambda e: e != leaf)
    print "Closest to leaf:", leaf, " is ", closest
    assert leaf != closest[0], "Entity searched from is not the one returned."

    print "Test find all in range."
    entities_in_range = spatial_index.find_all_in_range(leaf.location, 10000)
    print entities_in_range
    assert len(entities_in_range) == 2, "Correct number of entities in the field."

    print "Test removal of item"
    spatial_index.remove(leaf)
    print "Contents of cell 2,3:"
    print (spatial_index.spatial_index[2, 3])
    
    print spatial_index.which_cell((200, 300))

    print "Spatial Index Contents:"
    print spatial_index.spatial_index
    
    print "Doing benchmark insert."
    for leaf_no in xrange(10000):
        #Team 1
        leaf3 = MockLeaf(Vec2d(randint(0,global_data.world_size_x), randint(0, global_data.world_size_y)))
        spatial_index.update(leaf3)
            
    print "Doing benchmark search"
    for i in xrange(10000):
        closest, distance = spatial_index.find_closest(leaf.location, 100,
                                                       lambda e: e != leaf)
        
    print "Run complete."
    print closest, distance
