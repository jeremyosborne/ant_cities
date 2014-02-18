from src.common.ui.view import View, PositionableMixin, ScalableMixin

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

    v2.addchild(v)
    
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

    v2.addchild(v)
    
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

    v2.addchild(v)
    
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

    v2.addchild(v)
    
    assert v.contained_screenxy(point) == False, "Point not contained."
    assert v2.contained_screenxy(point) == False, "Point not contained."
    


def test_view_z_sorting():
    """Views should be sorted by zindex when they are childviews.
    """
    v = View(z=5)
    v2 = View(z=2)
    v3 = View(z=-1)
    v4 = View(z=3)
    
    vparent = View()
    
    vparent.addchild(v)
    vparent.addchild(v2)
    vparent.addchild(v3)
    vparent.addchild(v4)
    
    assert vparent.childviews[0] == v3, "Sorting is correct."
    assert vparent.childviews[1] == v2, "Sorting is correct."
    assert vparent.childviews[2] == v4, "Sorting is correct."
    assert vparent.childviews[3] == v, "Sorting is correct."

    vparent.removechild(v)
    
    assert len(vparent.childviews) == 3, "Childview correctly removed."
    
    v4.removeself()
    assert len(vparent.childviews) == 2, "Childview correctly removed."



def test_positionablemixin():
    class MockView(View, PositionableMixin):
        pass
    
    cv = MockView(x=10, y=15, width=20, height=30)
    pv = MockView(x=5, y=5, width=100, height=200)
    pv.addchild(cv)
    
    cv.position_relative_to_parent(x="left", y="top")
    assert cv.x == 0, "Correctly positioned."
    assert cv.y == 0, "Correctly positioned."
    
    cv.position_relative_to_parent(x="right")
    assert cv.x == 80, "Correctly positioned."    
    cv.position_relative_to_parent(x="right", buf=10)
    assert cv.x == 70, "Correctly positioned."
    
    cv.position_relative_to_parent(y="bottom")
    assert cv.y == 170, "Correctly positioned."
    cv.position_relative_to_parent(y="bottom", buf=10)
    assert cv.y == 160, "Correctly positioned."
    
    cv.position_relative_to_parent(x="center", y="center")
    assert cv.x == 40
    assert cv.y == 85
    cv.position_relative_to_parent(x="center", y="center", buf=3)
    assert cv.x == 43
    assert cv.y == 88
    
    cv.position_relative_to_parent(x=10, y=10, buf=10)
    assert cv.x == 20
    assert cv.y == 20
    
    cv.position_relative_to_parent(x=-5, y=-5, buf=5)
    assert cv.x == 70
    assert cv.y == 160
    

    # Error conditions.
    try:
        cv.position_relative_to_parent(x="top")
    except ValueError as err:
        pass
    assert err, "Correctly got an error."
    
    try:
        cv.position_relative_to_parent(y="left")
    except ValueError as err:
        pass
    assert err, "Correctly got an error."



def test_scalablemixin():
    class MockView(View, ScalableMixin):
        pass
    
    cv = MockView(x=10, y=15, width=20, height=30)
    pv = MockView(x=5, y=5, width=100, height=200)
    pv.addchild(cv)
    
    pv.scale_relative_to_parent(w=10, h=10)
    assert pv.width == 100, "Unchanged."
    assert pv.height == 200, "Unchanged."

    cv.scale_relative_to_parent(0, 0)
    assert cv.width == 0
    assert cv.height == 0
    
    cv.scale_relative_to_parent(1, 1)
    assert cv.width == 100
    assert cv.height == 200
    
    cv.scale_relative_to_parent(0.5, 2)
    assert cv.width == 50
    assert cv.height == 400

    # Error conditions.
    try:
        cv.scale_relative_to_parent(w=-1)
    except ValueError as err:
        pass
    assert err, "Correctly got an error."
    
    try:
        cv.scale_relative_to_parent(h=-1)
    except ValueError as err:
        pass
    assert err, "Correctly got an error."
    