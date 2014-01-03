import math
from src.commonmath import Heading



def test_heading():
    h = Heading()
    
    assert h.current == 0., "Expected default."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == 0., "Expected default."
    assert type(h.current_rad) == float, "Expected type."
    
    h.current = 90
    assert h.current == 90., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == math.pi/2, "Expected value."
    assert type(h.current_rad) == float, "Expected type."
    
    h.current = -90
    assert h.current == 270., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == math.pi*3/2, "Expected value."
    assert type(h.current_rad) == float, "Expected type."
    
    h.current = 360
    assert h.current == 0., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == 0., "Expected value."
    assert type(h.current_rad) == float, "Expected type."

    h.current = 0.
    h.current += 45.
    assert h.current == 45., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == math.pi/4, "Expected value."
    assert type(h.current_rad) == float, "Expected type."

    h.current_rad = math.pi/2
    assert h.current == 90., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == math.pi/2, "Expected value."
    assert type(h.current_rad) == float, "Expected type."
    
    h.current = 0
    h += 45
    assert h.current == 45., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == math.pi/4, "Expected value."
    assert type(h.current_rad) == float, "Expected type."

    h.current = 0
    h -= 90
    assert h.current == 270., "Expected value."
    assert type(h.current) == float, "Expected type."
    assert h.current_rad == 3*math.pi/2, "Expected value."
    assert type(h.current_rad) == float, "Expected type."
