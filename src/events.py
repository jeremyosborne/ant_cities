"""Event publisher/subscriber system.

Provides an event interface as well as a centralized event broadcast relay.

"""



class EventObject(dict):
    """ A bare object for returning event diagnostics.
    
    In general the following properties are to be expected:

    name {str} The name of the event.
    source {object} Generally the object that triggers the event.
    data {dict} Any labeled argument passed as data to the event publishing.
    """
    def __init__(self, name="unnamed", source=None, data=None):
        self.name = name
        self.source = source
        self.data = data or {}



class EventEmitter(object):
    """Implements a simple pub/sub interface.
    
    Suitable as a mixin or as a simple class.
    """
    def __init__(self):
        # Any listeners on the events. Is a hash of hashes.
        self._eventListeners = {}
    
    def __len__(self):
        """ Total number of event subscribers.
        """
        return sum(len(event_list) for event, event_list in self._eventListeners.items())

    def sub(self, event, callback):
        """ Subscribe to a named event.
        
        event {str} Name of the event to listen to.
        callback {function} Callback function that will be passed one argument:
        the EventObject.
        
        return {tuple} A key that can be used to unsubscribe this listener 
        from this event.
        """
        if event not in self._eventListeners:
            self._eventListeners[event] = []
        self._eventListeners[event].append(callback)
        
        # Should be considered opaque outside of the pub/sub world.
        return event, callback
    
    def pub(self, event, **kwargs):
        """ Publish an event.
        
        event {str} Name of the event to publish.
        target {mixed} Reference to object that should act as the target of
        the event.
        data {dict} Dictionary of data to be passed on to the listener.
        """
        if self._eventListeners.get(event):
            for listener in self._eventListeners.get(event):
                listener(EventObject(name=event, source=self, data=kwargs))

    def remove(self, event_key):
        """ Remove a specific event by key.
        
        event_key {tuple} An opaque key for removing events.
        """
        try:
            self._eventListeners.get(event_key[0]).remove(event_key[1])
        except Exception:
            # If there is no event to remove, don't explode.
            pass

    def removeall(self, event=None):
        """ Remove all events, or a particular group of events by name.
        
        event {str} The name of the event group to remove. If not passed,
        all events are removed.
        """
        if not event:
            # nominate all for gc
            self._eventListeners = {}
        else:
            try:
                del self._eventListeners[event]
            except KeyError:
                # allow silent fail for unsubscribed names.
                pass



# Make a centralized events interface, in case all want uniformity.
events = EventEmitter()

