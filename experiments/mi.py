"""Experiments using multiple inheritance for mixins.

Will a mixin that does not call super block calls to other methods?
"""

# If I want mixins that make use of init, I need to make sure all mixins
# assume other mixins might be part of the equation. This seems to defeat
# the mixin purpose. Sad face.
class TestMixin1(object):
    def __init__(self):
        super(TestMixin1, self).__init__()
        print "Init TestMixin1"

class TestMixin2(object):
    def __init__(self):
        super(TestMixin2, self).__init__()
        print "Init TestMixin2"

class TestMixin3(object):
    def __init__(self):
        super(TestMixin3, self).__init__()
        print "Init TestMixin3"
        
class Klassy(TestMixin1, TestMixin2, TestMixin3):
    def __init__(self):
        super(Klassy, self).__init__()

if __name__ == "__main__":
    k = Klassy()
    # After reading online, it looks like there are three patterns for mixins.
    # 1) A pattern that makes mixins somewhat like subclasses and require
    # the inheritors to call __init__.
    # 2) A mixin that, because it has no initialization requirements, applies
    # new properties and methods but does not require initialization.
    # 3) Mixins that also require some black magic through meta classes or
    # meta function tricks.
    #
    # After reviewing and some tests, I think pattern 1) and 2) are the best.
    # Pattern 3) would be good if I was building a framework, but at the moment
    # I'm not.
