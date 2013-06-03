"""
An class for implementing a viewport.
"""

class Viewport(object):
    """Manages various viewport abstractions."""
    def __init__(self, top=0, left=0, width=1024, height=768, scale=1):
        """Arguments assumed to be integers."""
        # The upper left anchor point of our viewport [left, top]
        self.anchor = [top, left]
        # The dimensions of our viewport as [width, height]
        # Assumed width and height are positive.
        self.size = [width, height]
        # Scales relative to 1 as default.
        self.scale = scale

    @property
    def top(self):
        """{int} The relative top coordinate offset."""
        return self.anchor[1]
    
    @top.setter
    def top(self, value):
        self.anchor[1] = value
    
    @property
    def left(self):
        """{int} The relative left coordinate offset."""
        return self.anchor[0]
    
    @left.setter
    def left(self, value):
        self.anchor[0] = value
    
    @property
    def right(self):
        """{int} The relative right coordinate (offset + width)."""
        return self.anchor[0] + self.size[0]

    @property
    def bottom(self):
        """{int} The relative bottom coordinate (offset + height)."""
        return self.anchor[1] + self.size[1]
    
    @property
    def width(self):
        return self.size[0]
    
    @width.setter
    def width(self, value):
        self.size[0] = value
    
    @property
    def height(self):
        return self.size[1]
    
    @height.setter
    def height(self, value):
        self.size[1] += value



if __name__ == "__main__":
    print "Testing..."
    v = Viewport()
    print "Initial viewport width: %s" % v.width
    print "Left anchor: %s" % v.left
    print "Right anchor: %s" % v.right
    print "Changing left anchor point by 100."
    v.left = 100
    print "Left anchor: %s" % v.left
    print "Right anchor: %s" % v.right

    print "Initial viewport height: %s" % v.height
    print "Top anchor: %s" % v.top
    print "Bottom anchor: %s" % v.bottom
    print "Changing top anchor point by 100."
    v.top = 100
    print "Top anchor: %s" % v.top
    print "Bottom anchor: %s" % v.bottom
