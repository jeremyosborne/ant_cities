from src.ui.view import View

def test_view_init():
    """View should be able to initialize correctly.
    """
    v = View(x=50, y=100, width=100, height=200)
    assert v.width == 100, "Width is accessible."
    assert v.height == 200, "Height is accessible."
    assert v.x == 50, "X offset is accessible."
    assert v.y == 100, "y offset is accessible."

def test_view_screenxy_offset():
    """View and nested views should be able to determine their screenxy offset.
    """
    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    # Before being nested.
    assert v.screenxy_offset() == (10, 20), "Assumes 0,0 as the default position from."
    assert v2.screenxy_offset() == (-5, 50), "Assumes 0,0 as the default position from."

    v2.add_childview(v)
    
    assert v.screenxy_offset() == (5, 70), "Parental offset is included."
    assert v2.screenxy_offset() == (-5, 50), "Children do not affect parent offset."

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

def test_view_screenxy_contained():
    """View can determine if a screen point is located within, even when nested.
    """
    v = View(x=10, y=20, width=10, height=10)
    v2 = View(x=-5, y=50, width=10, height=10)
    
    point = (11, 21)
    
    assert v.screenxy_contained(point) == True, "Point contained"
    assert v2.screenxy_contained(point) == False, "Point not contained."

    v2.add_childview(v)
    
    assert v.screenxy_contained(point) == False, "Point not contained."
    assert v2.screenxy_contained(point) == False, "Point not contained."
    

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
