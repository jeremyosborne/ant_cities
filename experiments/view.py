"""Practice code for views++.

As the UI of a game becomes more complex, we need a UI that is:
* Powerful enough to handle complex, layered interactions.
* Simple enough to work with and that uses concepts that can be grocked.

View should:
* Isolate the displaying of visual information in whatever medium we are
displaying on.
* Provide coordinate transforms between device coordinates and relative view
coordinates.
* Have a top and left coorinate for positioning that is relative to its parent
container.
* Allow optional nesting of views.
* Can determine if a coordinate is contained within a view container (for HMI 
pointer interactions).
* TODO: Allow all nested views the option of listening to an event publisher
(perhaps assume a controller is optionally passed in for all views).
* TODO: Allow optional modality, either explicitly or implicitly.

View should not:
* Perform any game logic.
* Be overly complex (no rebuilding the HTML dom).

Dependencies:
* pygame

"""

import pygame

class View(object):
    def __init__(self, x=0, y=0, width=0, height=0, **kwargs):
        """Initialize an instance.
        
        Position of view should be relative to parent.
        
        x {Number} Number of pixels offset from left (towards right if positive).
        y {Number} Number of pixels offset from top (towards bottom if possitive).
        width {Number} Number of wide.
        height {Number} Number of pixels tall.
        """
        # Dimensions stored as a rectangle.
        self.rect = pygame.Rect(x, y, width, height)

        # If None than this view has no parent.
        self.parent = None
        # Child views within this view hierarchy.
        self.childviews = []
        
        # Higher zindex, closer to the user (drawing happens later).
        self.zindex = kwargs.get("zindex") or 0
        
        self.subclass_init(**kwargs)

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
        view.parent = self

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
        view.parent = None
        
    def remove_self(self):
        """Remove a view from its parent, if it has a parent.
        
        Convenience method.
        """
        if self.parent:
            self.parent.remove_childview(self)

    def render(self, surface):
        """Begin the rendering process for this view and all child views.
        
        Should only be called on the lowest level (self.parent == None) view.
        
        surface {Surface} on which to render this view and all child views.
        """
        pass
    
    def draw_view(self, surface, offset=(0,0)):
        """Draw this specific view to the provided surface.
        
        Subclasses should override this to handle their specific drawing
        routines.
        
        surface {Surface} on which to render this view and all child views.        
        offset {tuple} Additional offset to apply to the top and left offset
        of this view for setting the rect.
        """
        pass

    def screenxy_to_relativexy(self, coord):
        """Convert a universal device coordinate to a relative xy coordinate.
        
        Takes into account view lineage (parents).

        coord {Indexable} An integer indexable item where [0] is the x 
        coordinate and [1] is the y coordinate equivalent. Coord is assumed to
        be an untranslated coordinate.
        
        returns an indexable coordinate relative to this rect.
        """
        pass

    def screenxy_contained(self, coord):
        """Determine if a device coordinate is contained within this view.
        
        Takes into account view lineage (parents).

        coord {Indexable} An integer indexable item where [0] is the x 
        coordinate and [1] is the y coordinate equivalent. Coord is assumed to
        be an untranslated coordinate.
        
        returns {bool} True if point is contained, False if not.
        """
        pass

    def screenxy_offset(self):
        """Determine the absolute offset from the universal device coordinate
        system of the top and left corner of this view.
        
        Example:
        This view has offset (10, 20).
        This view has a parent view with offset (-5, 50), which in turn has
        no parent.
        This function returns (5, 70).
        
        returns an indexable coordinate.
        """
        pass

