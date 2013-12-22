
class BrainState(object):
    def __init__(self, name):
        self.name = name
        self.entity = None
        
    def do_actions(self, time_passed):
        pass
        
    def check_conditions(self):
        pass
    
    def entry_actions(self):
        pass    
    
    def exit_actions(self):        
        pass



class Brain(object):
    def __init__(self, entity=None):
        self.states = {}
        # Which entity instance currently owns this brain?
        self.entity = entity
        self.active_state = None
    
    def add_state(self, state):
        self.states[state.name] = state
        # Side effect: set the owner of the behavior.
        state.entity = self.entity
        
    def think(self, time_passed):
        if self.active_state is None:
            return
        
        self.active_state.do_actions(time_passed)        

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()
            
        self.active_state = self.states[new_state_name]        
        self.active_state.entry_actions()

