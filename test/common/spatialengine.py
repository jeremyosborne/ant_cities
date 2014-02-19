import sys
sys.path = sys.path + ['/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/']

import time
from random import randint
from pymunk import Vec2d

from src.common.spatialengine import SpatialEngine

# Fixtures.
world_size_x = 1200*6
world_size_y = 530*6

class MockLeaf(object):
    id = 0
    def __init__(self, location):
        MockLeaf.id += 1
        self.id = MockLeaf.id
        self.location = location



def test_spatialengine_find_closest():
    spatial_index = SpatialEngine(world_size_x, world_size_y)
    leaf = MockLeaf(Vec2d(250, 350))
    leaf2 = MockLeaf(Vec2d(351, 451))    
    spatial_index.update(leaf)
    spatial_index.update(leaf2)
    #print "Contents of cell 2,3:"
    #print (spatial_index.spatial_index[2, 3])
    
    closest = spatial_index.find_closest(leaf.location, 100,
                                         lambda e: e != leaf)
    #print "Closest to leaf:", leaf, " is ", closest
    assert leaf != closest[0], "Entity searched from is not the one returned."



def test_spatialengine_find_all_in_range():
    spatial_index = SpatialEngine(world_size_x, world_size_y)
    leaf = MockLeaf(Vec2d(250, 350))
    leaf2 = MockLeaf(Vec2d(351, 451))    
    spatial_index.update(leaf)
    spatial_index.update(leaf2)
    
    entities_in_range = spatial_index.find_all_in_range(leaf.location, 10000)
    #print entities_in_range
    assert len(entities_in_range) == 2, "Correct number of entities in the field."



def test_spatialengine_remove():
    spatial_index = SpatialEngine(world_size_x, world_size_y)
    leaf = MockLeaf(Vec2d(250, 350))
    leaf2 = MockLeaf(Vec2d(351, 451))
    spatial_index.update(leaf)
    spatial_index.update(leaf2)

    spatial_index.remove(leaf)
    #print "Contents of spatial index:", spatial_index.spatial_index[2, 3]

    #print "Contents of spatial index:", spatial_index.which_cell((200, 300))

    # TODO: Write an actual tests here.


def test_spatialengine_benchmark_insert():
    spatial_index = SpatialEngine(world_size_x, world_size_y)
    num_items = 10000
    
    #print "BEGIN: Benchmark insert."
    start = time.time()
    for leaf_no in xrange(num_items):
        leaf = MockLeaf(Vec2d(randint(0, world_size_x), randint(0, world_size_y)))
        spatial_index.update(leaf)
    duration = time.time() - start
    #print "END: Benchmark insert. Time:", duration
    assert duration < 0.2, "Tolerable time to insert %s items." % num_items



def test_spatialengine_benchmark_search():
    spatial_index = SpatialEngine(world_size_x, world_size_y)
    num_items = 10000
    leaf = MockLeaf(Vec2d(250, 350))

    # TODO: Need to include the inserting of a lot of leaves.

    #print "BEGIN: benchmark search"
    start = time.time()
    for i in xrange(num_items):
        spatial_index.find_closest(leaf.location, 100,
                                   lambda e: e != leaf)
    duration = time.time() - start
    #print "END: Benchmark search. Time:", duration
    assert duration < 0.2, "Tolerable time to search through %s items." % num_items
