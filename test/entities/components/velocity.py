from src.entities.components.velocity import Velocity
from nose.tools import assert_almost_equal 
from src.commonmath import Heading
import math

def test_velocity():
    v = Velocity()
    
    v.speed = 0
    v.course = 90
    
    assert v.speed == 0., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == Heading(90.), "expected value"
    x, y = v.deltaxy
    assert x == 0., "expected value"
    assert type(x) == float, "expected type"
    assert y == 0., "expected value"
    assert type(y) == float, "expected type"
    
    v.speed = 1
    v.course = 45
    assert v.speed == 1., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == Heading(45.), "expected value"
    x, y = v.deltaxy
    # Unit circle values, and we're dealing with floating point.
    # Right is positive for x, left is negative.
    assert_almost_equal(x, math.sqrt(1-math.sin(math.pi/4)**2), 
                        msg="Expected value for x.")
    # Up is negative for y, down is positive.
    assert_almost_equal(y, -math.sqrt(1-math.cos(math.pi/4)**2), 
                        msg="Expected value for y.")

    v.speed = 2
    v.course = 135
    assert v.speed == 2., "expected value"
    assert type(v.speed) == float, "expected type"
    assert v.course == Heading(135.), "expected value"
    x, y = v.deltaxy
    # Unit circle values, and we're dealing with floating point.
    # Right is positive for x, left is negative.
    assert_almost_equal(x, 2*math.sqrt(1-math.sin(math.pi/4)**2), 
                        msg="Expected value for x.")
    # Up is negative for y, down is positive.
    assert_almost_equal(y, 2*math.sqrt(1-math.cos(math.pi/4)**2), 
                        msg="Expected value for y.")
