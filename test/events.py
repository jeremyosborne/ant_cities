from nose import with_setup
from src.events import EventEmitter

# Mock out an event emitter instance.
events = None
# Mock...
def setup():
    global events
    events = EventEmitter()
def teardown():
    global events
    events = None



@with_setup(setup, teardown)
def test_eventemitter_sub():
    """ Should be able to know how many total event subscriptions we have.
    """
    global events
    assert len(events) == 0, "By default, there are no events subscribed."
    events.sub("test", lambda x: x)
    assert len(events) == 1, "One event is subscribed."
    events.sub("test2", lambda x: x)
    assert len(events) == 2, "Two events subscribed to."
    events.sub("test2", lambda x: x)
    assert len(events) == 3, "Three events subscribed to."



@with_setup(setup, teardown)
def test_eventemitter_pub():
    """ Should be able to subscribe to an event and receive data.
    """
    global events
    
    def confirm_published(e):
        assert e.data["hello"] == "world", "Expected data received."
    
    events.sub("hello", confirm_published)
    events.pub("hello", hello="world")



@with_setup(setup, teardown)
def test_eventemitter_remove():
    """Should be able to remove an event that was previously subscribed to.
    """
    global events
    
    def to_be_removed(*args):
        assert False, "Should never see this."
    
    event_key = events.sub("hello", to_be_removed)
    assert len(events) == 1, "One event is subscribed."
    events.remove(event_key)
    assert len(events) == 0, "No events subscribed to."

    event_key = events.sub("hello", to_be_removed)
    events.sub("hello", lambda x: x)
    events.remove(event_key)
    assert len(events) == 1, "Can remove remove a single event."



@with_setup(setup, teardown)
def test_eventemitter_removeall():
    """Should be able to remove all events.
    """
    global events
    
    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert len(events) == 4, "4 total events subscribed."
    events.removeall()
    assert len(events) == 0, "No more events subscribed."



@with_setup(setup, teardown)
def test_eventemitter_removeall_named():
    """Should be able to remove groups of events by name.
    """
    global events

    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert len(events) == 4, "4 total events subscribed."
    events.removeall("test")
    assert len(events) == 2, "2 events subscribed."
    events.removeall("test1")
    assert len(events) == 1, "1 events subscribed."
    events.removeall("test2")
    assert len(events) == 0, "No more events subscribed."
