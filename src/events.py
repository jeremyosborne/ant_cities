"""Event publisher/subscriber system.

Provides an event interface as well as a centralized event broadcast relay.

"""

# What state is this module in?
_debug = False



class EventObject(dict):
    """A bare object for returning event diagnostics.
    
    In general the following properties are to be expected:
    
    target {object} Generally the object that triggers the event.
    """
    def __init__(self, **kwargs):
        self.target = kwargs.get("target") or None
        self.data = kwargs.get("data") or {}



class EventEmitter(object):
    """Implements a simple pub/sub interface.
    """
    def __init__(self):
        # Any listeners on the event.
        self._eventListeners = {}
        
    def sub(self, event, callback):
        """Subscribe to a named event.
        
        event {str} Name of the event to listen to.
        callback {function} Callback function that will be passed one argument:
        the EventObject.
        
        return the instance of the EventEmitter to allow chaining.
        """
        if event not in self._eventListeners:
            self._eventListeners[event] = []
        self._eventListeners[event].append(callback)
    
    def pub(self, event, data):
        """Publish an event.
        
        event {str} Name of the event to publish.
        data {dict} Dictionary of data to be passed on to the listener.
        """
        # Test for rogue publishing.
        assert self._eventListeners.get(event) if _debug == True else True, "Must have listeners before publishing."

        if self._eventListeners.get(event):
            for listener in self._eventListeners.get(event):
                listener(EventObject(target=self, data=data))



# Make a centralized events interface, in case all want uniformity.
events = EventEmitter()



if __name__ == "__main__":
    def functional_listen(e):
        assert e.data["hello"] == "world", "Expected data received."
        print "If you're seeing this, the assert passed:", e.data["hello"] == "world"

    # For testing, force asserts:
    _debug = True
 
    # Test with the basic interface.
    events.sub("hello", functional_listen)
    events.pub("hello", {"hello": "world"})
