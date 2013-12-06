from src.ui.view import View

def test_view_init():
    """View should be able to initialize correctly.
    """
    v = View(x=50, y=100, width=100, height=200)
    assert v.width == 100, "Width is accessible."
    assert v.height == 200, "Height is accessible."
    assert v.x == 50, "X offset is accessible."
    assert v.right == 150, "right is accessible."
    assert v.y == 100, "y offset is accessible."
    assert v.bottom == 300, "bottom is accessible."
    assert v.center == (50, 100), "center is correct, relative to self"
    assert v.center_screenxy == (100, 200), "center is correct relative to screen"

def test_view_centering():
    """View should correctly identify its center, even when contained.
    """
    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    # Before being nested.
    assert v.center_screenxy == (15, 25), "Correct center before nesting."
    assert v2.center_screenxy == (0, 55), "Correct center before nesting."

    v2.add_childview(v)
    
    assert v.center == (5, 5), "Correct relative center after nesting."
    assert v.center_screenxy == (10, 75), "Correct screen center after nesting."
    assert v2.center == (5, 5), "Correct relative center after nesting."
    assert v2.center_screenxy == (0, 55), "Correct screen center after nesting."


def test_view_screenxy_offset():
    """View and nested views should be able to determine their screenxy offset.
    """
    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    # Before being nested.
    assert v.offset_screenxy == (10, 20), "Assumes 0,0 as the default position from."
    assert v2.offset_screenxy == (-5, 50), "Assumes 0,0 as the default position from."

    v2.add_childview(v)
    
    assert v.offset_screenxy == (5, 70), "Parental offset is included."
    assert v2.offset_screenxy == (-5, 50), "Children do not affect parent offset."

def test_view_screenxy_to_relativexy():
    """View and nested views should be able to calculate points relative to
    themselves.
    """

    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    point = (10, 10)
    
    assert v.screenxy_to_relativexy(point) == (0, -10), "Point relative to view."
    assert v2.screenxy_to_relativexy(point) == (15, -40), "Point relative to view."

    v2.add_childview(v)
    
    assert v.screenxy_to_relativexy(point) == (5, -60), "Point relative to parent and self."
    assert v2.screenxy_to_relativexy(point) == (15, -40), "Point does not change with children."

def test_view_contained_screenxy():
    """View can determine if a screen point is located within, even when nested.
    """
    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    point = (11, 21)
    
    assert v.contained_screenxy(point) == True, "Point contained"
    assert v2.contained_screenxy(point) == False, "Point not contained."

    v2.add_childview(v)
    
    assert v.contained_screenxy(point) == False, "Point not contained."
    assert v2.contained_screenxy(point) == False, "Point not contained."
    

def test_view_zindex_sorting():
    """Views should be sorted by zindex when they are childviews.
    """
    v = View(zindex=5)
    v2 = View(zindex=2)
    v3 = View(zindex=-1)
    v4 = View(zindex=3)
    
    vparent = View()
    
    vparent.add_childview(v)
    vparent.add_childview(v2)
    vparent.add_childview(v3)
    vparent.add_childview(v4)
    
    assert vparent.childviews[0] == v3, "Sorting is correct."
    assert vparent.childviews[1] == v2, "Sorting is correct."
    assert vparent.childviews[2] == v4, "Sorting is correct."
    assert vparent.childviews[3] == v, "Sorting is correct."

    vparent.remove_childview(v)
    
    assert len(vparent.childviews) == 3, "Childview correctly removed."
    
    v4.remove_self()
    assert len(vparent.childviews) == 2, "Childview correctly removed."
