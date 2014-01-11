'''
Created on Oct 20, 2013

@author: john
'''

import math

class SpatialEngine(object):
    """Coarser spatial storage for entities using 2d points for location.
    """
    def __init__(self, world_size_x, world_size_y):
        """Constructor.
        
        world_size_x {int} number of pixels wide the world is.
        world_size_y {int} number of pixels hight he world is.
        """
        # Edge length of a cell (width and height). Cells are square.
        self.cell_size = 100
        
        # Spatial index keyed with 
        self.spatial_index = {}
        # key == entity.id, value = cell containing entity
        self.entity_index = {}
        
        # Seed the spatial index to fit our world. Errs larger than needed.
        width = int(math.ceil(world_size_x/float(self.cell_size))+1)
        height = int(math.ceil(world_size_y/float(self.cell_size))+1)
        for i in range(width):
            for j in range(height):
                self.spatial_index[i,j] = []

    def _insert(self, entity):
        """Add an entity to the spatial index.
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
        """Remove an entity from the spatial index.
        
        entity {entity} Must provide a .id attribute uniquely identifying the
        entity.
        """
        if entity.id in self.entity_index:
            cell = self.entity_index[entity.id]
            self.spatial_index[cell].remove(entity)
            # delete lookup by id
            del self.entity_index[entity.id]
    
    def update(self, entity):
        """Update an entity's location within the spatial index.
        
        entity {entity} Must provide a .id and .location interface to the 2d location
        of the entity.
        """
        self.remove(entity)
        self._insert(entity)

    def which_cell(self, point):
        """Identifies which cell a coordinate belongs to.

        point {tuple} Unpackable 2d coordinate in the form of (x, y).
        
        return {tuple} Cell identifier.
        """
        x = int(point[0] / self.cell_size)
        y = int(point[1] / self.cell_size)
        return (x, y)
    
    def which_cells_in_range(self, point, the_range):
        """Given a point and a search radius, return the list of
        cells that should be considered.
        
        point {tuple} Unpackable 2d coordinate in the form of (x, y).
        the_range {number} How many pixels radius in which to search.
        
        return {list} List of identifiers in the form of.
        """
        x, y = point
        # Determine the area we should be looking at.
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
        """Returns list of all entities in range.

        point {Vec2d} Location to search from.
        [the_range=5.0] {float} Number of pixels radius to allow for a match.
        [validate] {function} If included, filters out possible results.

        return {Entity[]} any entities in range, or an empty list.
        """
        cell_list = self.which_cells_in_range(point, the_range)
        entities = []
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
        """Find the closest entity.
        
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



