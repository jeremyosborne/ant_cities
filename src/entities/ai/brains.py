
class BrainState(object):
    """Explicit states that a brain might be in.
    """
    def __init__(self, name):
        """Initialize a new instance.
        
        name {str} The human friendly name of this state. Used for reference
        and indexing.
        """
        self.name = name
        # {Entity} Reserve property for entity that this state is attached to.
        self.entity = None
        
    def process(self, time_passed):
        """Called each moment this state can be processed.
        
        time_passed {float} Number of seconds since this function was last
        called.
        
        returns {str} which is the name of the state we should transition to
        or {None} if we should not transition to another new state.
        """
        pass

    def entry_actions(self):
        """Called when this state is entered.
        """
        pass    
    
    def exit_actions(self):
        """Called when the brain transitions out of this state into a new one.
        """
        pass



class Brain(object):
    """Brains belong to entities, and perform as a simple, finite state machine.
    """
    def __init__(self, entity=None):
        """Initialize the brain.
        
        entity {Entity} What owns this brain?
        """
        # Available states indexed by name.
        self.states = {}
        # Which entity instance currently owns this brain?
        self.entity = entity
        # What is the currently set state?
        self.active_state = None
    
    def add_state(self, state):
        """Add another state to this brain.
        
        Default brains start off with no states.
        """
        self.states[state.name] = state
        # Side effect: set the owner of the behavior.
        state.entity = self.entity
        
    def process(self, time_passed):
        """Process the current state and determine if there is a state
        transition.
        
        time_passed {float} Number of seconds since the last time this was
        called.
        """
        if self.active_state is None:
            return

        new_state_name = self.active_state.process(time_passed)
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    def set_state(self, new_state_name):
        """Transition from one state to the next.
        
        Should be called to set the first active_state.
        
        new_state_name {str} Key to the new state. Must be a valid state name,
        or None which will make the current state nothing.
        """
        if self.active_state is not None:
            self.active_state.exit_actions()
        
        if new_state_name is not None:
            self.active_state = self.states[new_state_name]        
            self.active_state.entry_actions()
        else:
            self.active_state = None


