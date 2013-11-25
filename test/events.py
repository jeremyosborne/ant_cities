from nose import with_setup
from src.events import EventPublisher

# Mock out an event instance.
events = None
# Mock...
def setup():
    global events
    events = EventPublisher()
def teardown():
    global events
    events = None



@with_setup(setup, teardown)
def test_eventpubslisher_sub():
    """Should be able to subscribe and know many event subscriptions we have.
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
def test_eventpubslisher_pub():
    """Should be able to subscribe to receive data when event is published.
    """
    global events
    
    def listener(e):
        # test event object
        assert e.name == "hello", "name attr provides name of event published."
        assert e.source == events, "source attr points to publisher of event."
        assert e.data == {"hello": "world"}, "data attr provides expected data."
    
    events.sub("hello", listener)
    events.pub("hello", hello="world")



@with_setup(setup, teardown)
def test_eventpublisher_clear():
    """Should be able to remove event listeners.
    """
    global events
    
    def to_be_cleared(*args):
        assert False, "Listener should not be called, hence auto fail test."
    
    event_key = events.sub("hello", to_be_cleared)
    assert len(events) == 1, "One event is subscribed."
    events.clear_one(event_key)
    assert len(events) == 0, "No events subscribed to."

    event_key = events.sub("hello", to_be_cleared)
    events.sub("hello", lambda x: x)
    events.clear_one(event_key)
    assert len(events) == 1, "Confirm one event is removed."



@with_setup(setup, teardown)
def test_eventpublisher_clear_all():
    """Should be able to remove all event listeners at once.
    """
    global events
    
    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert len(events) == 4, "4 total events subscribed."
    events.clear_many()
    assert len(events) == 0, "No more events subscribed."



@with_setup(setup, teardown)
def test_eventpublisher_clear_by_group():
    """Should be able to remove event listeners by event name.
    """
    global events

    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert len(events) == 4, "4 total events subscribed."
    events.clear_many("test")
    assert len(events) == 2, "2 events subscribed."
    events.clear_many("test1")
    assert len(events) == 1, "1 events subscribed."
    events.clear_many("test2")
    assert len(events) == 0, "No more events subscribed."
