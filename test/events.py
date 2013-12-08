from nose import with_setup
from src.events import EventPublisher, EventSubscriber


#-----------------------------------------------------------------------------
# Mock out an event instance.
events = None
# Can be used by tests to assert things have run, count tests.
asserted = False
# Mock...
def eventpublisher_setup():
    global events
    events = EventPublisher()
def eventpublisher_teardown():
    global events, asserted
    events = None
    asserted = False



@with_setup(eventpublisher_setup, eventpublisher_teardown)
def test_eventpubslisher_sub():
    """Should be able to subscribe and know many event subscriptions we have.
    """
    global events
    assert events.countsubs() == 0, "By default, there are no events subscribed."
    events.sub("test", lambda x: x)
    assert events.countsubs() == 1, "One event is subscribed."
    events.sub("test2", lambda x: x)
    assert events.countsubs() == 2, "Two events subscribed to."
    events.sub("test2", lambda x: x)
    assert events.countsubs() == 3, "Three events subscribed to."



@with_setup(eventpublisher_setup, eventpublisher_teardown)
def test_eventpubslisher_pub():
    """Should be able to subscribe to receive data when event is published.
    """
    global events
    
    def listener(e):
        global asserted
        # test event object
        assert e.name == "hello", "name attr provides name of event published."
        assert e.source == events, "source attr points to publisher of event."
        assert e.data == {"hello": "world"}, "data attr provides expected data."
        asserted = True
    
    events.sub("hello", listener)
    events.pub("hello", hello="world")

    assert asserted == True, "callback called, we ran the tests."


@with_setup(eventpublisher_setup, eventpublisher_teardown)
def test_eventpublisher_clear():
    """Should be able to remove event listeners.
    """
    global events
    
    def to_be_cleared(*args):
        assert False, "Listener should not be called, auto fail test."
    
    event_key = events.sub("hello", to_be_cleared)
    assert events.countsubs() == 1, "One event is subscribed."
    events.clear_one(event_key)
    assert events.countsubs() == 0, "No events subscribed to."

    event_key = events.sub("hello", to_be_cleared)
    events.sub("hello", lambda x: x)
    events.clear_one(event_key)
    assert events.countsubs() == 1, "Confirm one event is removed."



@with_setup(eventpublisher_setup, eventpublisher_teardown)
def test_eventpublisher_clear_all():
    """Should be able to remove all event listeners at once.
    """
    global events
    
    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert events.countsubs() == 4, "4 total events subscribed."
    events.clear_many()
    assert events.countsubs() == 0, "No more events subscribed."



@with_setup(eventpublisher_setup, eventpublisher_teardown)
def test_eventpublisher_clear_by_group():
    """Should be able to remove event listeners by event name.
    """
    global events

    events.sub("test", lambda x: x)
    events.sub("test", lambda x: x)
    events.sub("test1", lambda x: x)
    events.sub("test2", lambda x: x)
    assert events.countsubs() == 4, "4 total events subscribed."
    events.clear_many("test")
    assert events.countsubs() == 2, "2 events subscribed."
    events.clear_many("test1")
    assert events.countsubs() == 1, "1 events subscribed."
    events.clear_many("test2")
    assert events.countsubs() == 0, "No more events subscribed."



#-----------------------------------------------------------------------------
# Mock out objects
eventpub = None
eventsub = None
# Mock...
def eventsubscriber_setup():
    global eventpub, eventsub
    eventpub = EventPublisher()
    eventsub = EventSubscriber()
def eventsubscriber_teardown():
    global eventpub, eventsub, asserted
    eventpub = None
    eventsub = None
    # Reuse from above.
    asserted = False

@with_setup(eventsubscriber_setup, eventsubscriber_teardown)
def test_eventsubscriber():
    """Should be able to subto event publishers.
    """
    global eventpub, eventsub
    
    def listener(e):
        global asserted
        # test event object
        assert e.name == "test-event", "name attr provides name of event published."
        assert e.source == eventpub, "source attr points to publisher of event."
        assert e.data == {"hello": "world"}, "data attr provides expected data."
        asserted = True
    
    eventsub.subto(eventpub, "test-event", listener)
    assert eventpub.countsubs() == 1, "Event pub has registered event listener."
    
    eventpub.pub("test-event", hello="world")
    assert asserted == True, "The event listener was called."
    
    eventsub.unsubfrom("test-event")
    assert eventpub.countsubs() == 0, "Event pub has unregistered event listener."
    
    