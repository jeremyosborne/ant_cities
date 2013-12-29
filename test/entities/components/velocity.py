from src.entities.components.velocity import Velocity
from nose.tools import assert_almost_equal 
import math

def test_heading():
    v = Velocity()
    
    v.speed = 0
    v.course = 90
    assert v.speed == 0., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == 90., "expected value"
    assert type(v.course) == float, "expected type"
    assert v.x == 0., "expected value"
    assert type(v.x) == float, "expected type"
    assert v.y == 0., "expected value"
    assert type(v.y) == float, "expected type"
    
    v.speed = 1
    v.course = 45
    assert v.speed == 1., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == 45., "expected value"
    assert type(v.course) == float, "expected type"
    # Unit circle values, and we're dealing with floating point.
    # Right is positive for x, left is negative.
    assert_almost_equal(v.x, math.sqrt(1-math.sin(math.pi/4)**2), 
                        msg="Expected value for x.")
    # Up is negative for y, down is positive.
    assert_almost_equal(v.y, -math.sqrt(1-math.cos(math.pi/4)**2), 
                        msg="Expected value for y.")

    v.speed = 2
    v.course = 135
    assert v.speed == 2., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == 135., "expected value"
    assert type(v.course) == float, "expected type"
    # Unit circle values, and we're dealing with floating point.
    # Right is positive for x, left is negative.
    assert_almost_equal(v.x, 2*math.sqrt(1-math.sin(math.pi/4)**2), 
                        msg="Expected value for x.")
    # Up is negative for y, down is positive.
    assert_almost_equal(v.y, 2*math.sqrt(1-math.cos(math.pi/4)**2), 
                        msg="Expected value for y.")
