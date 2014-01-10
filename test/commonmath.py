import math
from src.commonmath import mmval, courseto, distanceto, Heading



def test_mmval():
    assert mmval(100, 10, 0) == 10, "Expected value."
    assert mmval(100, 10) == 10, "Expected value."
    assert mmval(100, -10) == 0, "Expected value."
    assert mmval(100, -10, -25) == -10, "Expected value."
    assert mmval(100, 110, -25) == 100, "Expected value."

def test_courseto():
    # NOTE: These results are different than Cartesian coordinates 
    # due to inverted y signage (e.g. down and right is positive for both
    # x and y).
    assert courseto((0, 0), (0, -1)) == 0, "Correct screen coordinate course."
    assert courseto((0, 0), (1, -1)) == 45, "Correct screen coordinate course."
    assert courseto((0, 0), (1, 0)) == 90, "Correct screen coordinate course."
    assert courseto((0, 0), (1, 1)) == 135, "Correct screen coordinate course."
    assert courseto((0, 0), (0, 1)) == 180, "Correct screen coordinate course."
    assert courseto((0, 0), (-1, 1)) == 225, "Correct screen coordinate course."
    assert courseto((0, 0), (-1, 0)) == 270, "Correct screen coordinate course."
    assert courseto((0, 0), (-1, -1)) == 315, "Correct screen coordinate course."

    # NOTE: This is a default value, weird as it is.
    assert courseto((0, 0), (0, 0)) == 90, "Expected but arbitrary value."

    
def test_distanceto():
    assert distanceto((-1, 1), (1, 1)) == 2, "Expected distance."
    assert distanceto((0, 0), (0, 0)) == 0, "Expected distance."

def test_heading():
    h = Heading()
    
    assert h.deg == 0., "Expected default."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == 0., "Expected default."
    assert type(h.rad) == float, "Expected type."
    
    h.deg = 90
    assert h.deg == 90., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == math.pi/2, "Expected value."
    assert type(h.rad) == float, "Expected type."
    
    h.deg = -90
    assert h.deg == 270., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == math.pi*3/2, "Expected value."
    assert type(h.rad) == float, "Expected type."
    
    h.deg = 360
    assert h.deg == 0., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == 0., "Expected value."
    assert type(h.rad) == float, "Expected type."

    h.deg = 0.
    h.deg += 45.
    assert h.deg == 45., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == math.pi/4, "Expected value."
    assert type(h.rad) == float, "Expected type."

    h.rad = math.pi/2
    assert h.deg == 90., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == math.pi/2, "Expected value."
    assert type(h.rad) == float, "Expected type."
    
    h.deg = 0
    h += 45
    assert h.deg == 45., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == math.pi/4, "Expected value."
    assert type(h.rad) == float, "Expected type."

    h.deg = 0
    h -= 90
    assert h.deg == 270., "Expected value."
    assert type(h.deg) == float, "Expected type."
    assert h.rad == 3*math.pi/2, "Expected value."
    assert type(h.rad) == float, "Expected type."

    h2 = Heading(45.)
    h3 = Heading(45.)
    assert h2 == h3, "Should be equal."
    assert h2 == 45., "Should be equal."
    assert h2 != 40, "Should not be equal."
    
    h4 = Heading(360.)
    h5 = Heading(0.)
    assert h4 == h5, "Should be equal."
    assert h4 != 360., "Should not be equal."
    assert h4 != 360, "Should not be equal."
    h5 += 0.5
    assert h4 != h5, "Should not be equal."
    
    h6 = Heading(360.)
    h7 = Heading(275.)
    assert h6 <= 0., "Is true."
    assert h6 < h7, "Correctly True (360 rotates back to zero)."
    assert h6 < 360, "Treat numbers literally."
    assert (h7 < 275) == False, "Is truely false."

    assert h6 >= 0., "Is True."
    assert (h6 > 0) == False, "Is truely false."
    
    h8 = Heading(15)
    h9 = Heading(180)
    h8.set(h9)
    assert h8 == h9, "Now equal."
    assert h9 == 180, "Now equal."
    
    assert Heading(0).angleto(359) == -1, "Shortest angle."
    assert Heading(359).angleto(0) == 1, "Shortest angle."
    assert Heading(1).angleto(2) == 1, "Shortest angle."
    assert Heading(0).angleto(181) == -179, "Shortest angle."
