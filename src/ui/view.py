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
* TODO: Allow relative (to parent) positioning via mixin.
* TODO: Allow relative (to parent) sizing via mixin.

A View should not:
* Perform any game logic.
* Perform modality. Modality and overall view state should be handled by the
controller.
"""

class PositionableMixin(object):
    def positionToParent(self):
        pass

class SizableMixin(object):
    def sizeToParent(self):
        pass

class View(object):
    def __init__(self, x=0, y=0, width=0, height=0, zindex=0, controller=None, **kwargs):
        """Initialize an instance.
        
        Position of view should be relative to parent.
        
        x {Number} Number of pixels offset from left (towards right if positive).
        y {Number} Number of pixels offset from top (towards bottom if possitive).
        width {Number} Number of wide.
        height {Number} Number of pixels tall.
        zindex {int} Higher number, the later the UI is drawn.
        controller {EventPublisher} An object that should implement a pubsub
        interface, as well as any other methods for handling communication to
        and from the UI.
        """
        # All properties are shadowed.
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Higher zindex, closer to the user (drawing happens later).
        self.zindex = zindex

        # For each View a surface.
        # RESERVED for setting within the subclass_init.
        self.surface = None

        # If None than this view has no parent.
        self.parentView = None
        # Child views within this view hierarchy.
        self.childviews = []

        # Assumes mixins do not require arguments.
        super(View, self).__init__()
        self.subclass_init(**kwargs)

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
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    def subclass_init(self, **kwargs):
        """For subclasses to override, called by __init__. 
        
        Any kwargs to __init__ are passed as kwargs here.
        """
        pass
    
    def add_childview(self, view):
        """Delegate a view to this view hierarchy.
        
        view {View} to be added.
        """
        self.childviews.append(view)
        self.sort_childviews()
        view.parentView = self

    def sort_childviews(self):
        """Sort the existing childviews.
        
        Default is sorting by zindex of childviews in ascending order (higher
        zindex rendered last/closer to user.) Keeping all childviews with
        the same index will enforce the rendering in the roder added.
        """
        self.childviews = sorted(self.childviews, key=lambda cv: cv.zindex)

    def remove_childview(self, view):
        """Remove a view from this view hierarchy.
        
        view {View} to be removed.
        """
        self.childviews.remove(view)
        # No resorting, assumes removing does not change indexing.
        view.parentView = None
        
    def remove_self(self):
        """Remove a view from its parent, if it has a parent.
        
        Convenience method.
        """
        if self.parentView:
            self.parentView.remove_childview(self)

    def render(self, surface):
        """Begin the rendering process for this view and all child views.
        
        surface {Surface} on which to render this view and all child views.
        """
        self.draw_view(surface)
        for v in self.childviews:
            v.draw_view(surface)
    
    def draw_view(self, surface):
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
        offset = self.screenxy_offset()
        return (coord[0]-offset[0], coord[1]-offset[1])

    def screenxy_contained(self, coord):
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

    def screenxy_offset(self):
        """Determine the absolute offset from the universal device coordinate
        system of the top and left corner of this view.
        
        Example:
        This view has offset (10, 20).
        This view has a parent view with offset (-5, 50), which in turn has
        no parent.
        This function returns (5, 70).
        
        returns {tuple} an indexable coordinate.
        """
        offset = [self.x, self.y]
        ancestor = self.parentView
        while ancestor:
            offset[0] += ancestor.x
            offset[1] += ancestor.y
            ancestor = ancestor.parentView

        return tuple(offset)
