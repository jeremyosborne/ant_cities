from src.events import events



def test_simple_pub():
    """ Make sure that the simplest of events can be subscribed to and that
    communication happens.
    """
    def confirm_published(e):
        assert e.data["hello"] == "world", "Expected data received."
    events.sub("hello", confirm_published)
    events.pub("hello", {"hello": "world"})
