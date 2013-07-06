'''
Created on Jul 5, 2013

@author: john
'''

import pymunk
from pymunk.vec2d import Vec2d

if __name__ == '__main__':

    origin_point = Vec2d(100, 100)
    destination1 = Vec2d(200, 0)
    destination2 = Vec2d(100, 200)
    
    vec_to_destination1 = destination1 - origin_point
    vec_to_destination2 = destination2 - origin_point
    
    angle = vec_to_destination1.get_angle_degrees_between(vec_to_destination2)
    
    print "Non normalized:" , angle
    
    vec1 = vec_to_destination1.normalized()
    vec2 = vec_to_destination2.normalized()
    
    angle2 = vec1.get_angle_degrees_between(vec2)
    
    print "Normalized: ", angle2

    vec1 = Vec2d(0.0, -1.0)
    print "vec1: ", vec1    
    print "Rotated vector: ", vec1.rotated_degrees(11.8)
    print "vec1: ", vec1
    
    print vec1.x
    print vec1.y