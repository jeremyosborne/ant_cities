"""UI scaffolding.

As the UI of a game becomes more complex, we need a UI that is:
* Powerful enough to handle complex, layered interactions.
* Simple enough to work with and that uses concepts that can be grocked.

A View should:
* Isolate the displaying of visual information in whatever medium we are
displaying on.
* Provide coordinate transforms between device coordinates and relative view
coordinates.
* Have a top and left coorinate for positioning that is relative to its parent
container.
* Allow optional nesting of views.
* Can determine if a coordinate is contained within a view container (for HMI 
pointer interactions).
* Views will listen to events through their associated controller.
* Allow relative (to parent) positioning via mixin.
* Allow relative (to parent) scaling via mixin.

A View should not:
* Perform any game logic.
* Perform modality. Modality and overall view state should be handled by the
controller.
"""



class PositionableMixin(object):
    """Helpers used to position view.
    """
    def position_relative_to_parent(self, x=None, y=None, buf=0):
        """Position relative to parent, if parent is available.
        
        Aids positioning that would likely require reusable math.
        
        x {mixed} The following arguments are supported:
            None = Do not position this property.
            "right" = Position right hand side of this view relative to right
            side of parent view.
            "left" = Position left hand side of this view relative to left
            side of parent view.
            "center" = Position view centered horizontally.
            0...n = Position left of view x number of pixels from the
            left of parent view.
            -1...-n = Position right of view x number of pixels from the
            right of parent view.
        y {mixed} The following arguments are supported:
            None = Do not position this property.
            "top" = Position top side of this view relative to top side of
            parent view.
            "bottom" = Position bottom side of this view relative to bottom side
            of parent view.
            "center" = Position view centered vertically.
            0...n = Position top of view x number of pixels from the
            top of parent view.
            -1...-n = Position bottom of view x number of pixels from
            the bottom of parent view.
        buf {int} A buffer that will add extra padding relative to the sort
        of positioning being performed. If a number, will apply to both x and
        y. If a tuple, will [0] applies to x, [1] applies to y.
        
        raises ValueError if an incorrect value is passed to any parameter.
        """
        if not self.parentview:
            # No parent to position relative to.
            return
        parent = self.parentview
        
        # Handle buffer.
        if type(buf) == tuple:
            bufx = buf[0]
            bufy = buf[1]
        else:
            bufx = bufy = buf
        
        if x == "left":
            self.x = 0 + bufx
        elif x == "right":
            self.x = parent.width - self.width - bufx
        elif x == "center":
            # Buffer, if applied, pushes in positive direction.
            self.x = parent.center[0] - self.width/2 + bufx
        elif type(x) == int and x < 0:
            # Because this number is negative, we need to reverse signage.
            self.x = parent.width - self.width + x - bufx
        elif type(x) == int and x >= 0:
            self.x = x + bufx
        elif x:
            raise ValueError("Unexpected value for x: %s" % x)
        
        if y == "top":
            self.y = 0 + bufy
        elif y == "bottom":
            self.y = parent.height - self.height - bufy
        elif y == "center":
            # Buffer, if applied, pushes in positive direction.
            self.y = parent.center[1] - self.height/2 + bufy
        elif type(y) == int and y < 0:
            # Because this number is negative, we need to reverse signage.
            self.y = parent.height - self.height + y - bufy
        elif type(y) == int and y > 0:
            self.y = y + bufy
        elif y:
            raise ValueError("Unexpected value for y: %s" % y)



class ScalableMixin(object):
    """Helpers used to scale the view.
    """
    def scale_relative_to_parent(self, w=None, h=None):
        """Set the size of the view relative to the parent size. Fractions
        rounded down.
        
        w {float} Scalar applied to element width relative to parent width.
        h {float} Scalar applied to element height relative to parent height.

        raises ValueError if an incorrect value is passed to any parameter.
        """
        if not self.parentview:
            # No parent to position relative to.
            return
        parent = self.parentview
        
        if (type(w) == float or type(w) == int) and w >= 0:
            self.width = parent.width * w
        elif w:
            raise ValueError("Unexpected value for w: %s" % w)

        if (type(h) == float or type(h) == int) and h >= 0:
            self.height = parent.height * h
        elif h:
            raise ValueError("Unexpected value for h: %s" % h)



class View(object):
    
    # Reserved. Abstract surface to be implemented by instances or subclasses.
    surface = None
    
    # Default cache values initialized.
    _x = 0
    _y = 0
    _z = 0
    _width = 0
    _height = 0
    
    def __init__(self, x=0, y=0, width=0, height=0, z=0, controller=None, **kwargs):
        """Initialize an instance.
        
        Position of view should be relative to parent.
        
        x {Number} Number of pixels offset from left (towards right if positive).
        y {Number} Number of pixels offset from top (towards bottom if possitive).
        width {Number} Number of wide.
        height {Number} Number of pixels tall.
        z {int} Higher number, the later the UI is drawn.
        controller {EventPublisher} An object that should implement a pubsub
        interface, as well as any other methods for handling communication to
        and from the UI.
        """
        # Access to our controller.
        self.controller = controller
        
        # All properties are shadowed and assumed to be overridden in
        # subclasses (e.g. trigger resizing of other properties on dimension
        # change).
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        # Higher z, closer to the user (drawing happens later).
        self._z = z

        # If None than this view has no parent.
        self.parentview = None
        # Child views within this view hierarchy.
        self.childviews = []
        
        # Assumes mixins don't want arguments. This might be a bad assumption.
        super(View, self).__init__()
        self.subclass_init(**kwargs)

    # Assumes subclasses override computed property to resize
    # on dimension change.
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        
    @property
    def right(self):
        """Shorthand for x+width.
        """
        return self.x+self.width

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    @property
    def bottom(self):
        """Shorthand for y+height.
        """
        return self.y+self.height

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

    @property
    def center(self):
        """{tuple} Center coordinate relative to this view.
        """
        return (self.width/2, self.height/2)
    
    @property
    def center_screenxy(self):
        """{tuple} Center coordinate relative to the screen. Views with no 
        parent are assumed to be placed relative to the screen.
        """
        offset = self.offset_screenxy
        return (offset[0]+self.width/2, offset[1]+self.height/2)

    @property
    def offset_screenxy(self):
        """{tuple} The absolute offset from the universal device coordinate
        system of the top and left corner of this view.
        
        Example:
        This view has offset (10, 20).
        This view has a parent view with offset (-5, 50), which in turn has
        no parent.
        This function returns (5, 70).
        """
        x, y = self.x, self.y
        ancestor = self.parentview
        while ancestor:
            x += ancestor.x
            y += ancestor.y
            ancestor = ancestor.parentview

        return (x, y)

    def subclass_init(self, **kwargs):
        """For subclasses to override, called by __init__. 
        
        Any kwargs to __init__ are passed as kwargs here.
        """
        pass
    
    def addchild(self, view):
        """Delegate a view to this view hierarchy.
        
        view {View} to be added.
        """
        self.childviews.append(view)
        self.sortchildren()
        view.parentview = self
        # Allow an element to position itself relatively now that it knows
        # its parent.
        view.position()
    
    def position(self):
        """Position the element with all known information.
        
        Will be called automatically on child views after they have been
        added to their parent.
        """
        pass

    def sortchildren(self):
        """Sort the existing childviews.
        
        Default is sorting by z of childviews in ascending order (higher
        z rendered last/closer to user.) Keeping all childviews with
        the same index will enforce the rendering in the roder added.
        """
        self.childviews = sorted(self.childviews, key=lambda cv: cv.z)

    def removechild(self, view):
        """Remove a view from this view hierarchy.
        
        view {View} to be removed.
        """
        self.childviews.remove(view)
        # No resorting, assumes removing does not change indexing.
        view.parentview = None
        
    def removeself(self):
        """Remove a view from its parent, if it has a parent.
        
        Convenience method.
        """
        if self.parentview:
            self.parentview.removechild(self)

    def render(self, surface=None):
        """Begin the rendering process for this view and all child views.
        
        surface {Surface} on which to render this view and all child views.
        """
        self.clear()
        for v in self.childviews:
            # Child views draw themselves on our surface...
            v.render(self.surface)
        # ...and then we draw anything remaining for ourselves as well as
        # draw ourselves on the provided surface.
        self.draw(surface)
    
    def clear(self):
        """Erase our own surface.
        
        Implement on subclasses.
        """
        pass
    
    def draw(self, surface):
        """Draw this specific view to the provided surface.
        
        Subclasses should override this to handle their specific drawing
        routines.
        
        surface {Surface} on which to render this view and all child views.        
        """
        pass

    def screenxy_to_relativexy(self, coord):
        """Convert a universal device coordinate to a relative xy coordinate.
        
        Takes into account view lineage (parents).

        coord {Indexable} An integer indexable item where [0] is the x 
        coordinate and [1] is the y coordinate equivalent. Coord is assumed to
        be an untranslated coordinate.
        
        returns {tuple} an indexable coordinate relative to this rect.
        """
        offset = self.offset_screenxy
        return (coord[0]-offset[0], coord[1]-offset[1])

    def contained_screenxy(self, coord):
        """Determine if a device coordinate is contained within this view.
        
        Takes into account view lineage (parents).

        coord {Indexable} An integer indexable item where [0] is the x 
        coordinate and [1] is the y coordinate equivalent. Coord is assumed to
        be an untranslated coordinate.
        
        returns {bool} True if point is contained, False if not.
        """
        x, y = self.screenxy_to_relativexy(coord)
        # Need just a width and height check.
        return (0 <= x and x <= self.width and 0 <= y and y <= self.height)

