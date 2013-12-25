"""Generate a runtime unique id.
"""

# The next id that will be handed out.
_next_id = 0L

def gen():
    """Return the next application-unique id.
    """
    global _next_id
    _next_id += 1
    return _next_id
