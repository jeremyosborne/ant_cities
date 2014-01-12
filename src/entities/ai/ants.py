from random import randint
from entities.ai.brains import BrainState



class Exploring(BrainState):
    
    # At what percentage will we attempt to go get energy.
    energy_depleted = .25
    
    # How many ticks between when we search for leaves?
    leaf_search_period = 17

    # What is the search radius for finding things?
    sight = 500.

    # Allows things to be done not-every frame. Should be reset on enter.
    tick_counter = 0
    
    def __init__(self):
        BrainState.__init__(self, "exploring")        
        
    def set_random_destination(self):
        p = (randint(0, self.entity.world.width), randint(0, self.entity.world.height))
        self.entity.c["destination"].set(p)
        
    def process(self, time_passed):
        # Requires a destination component
        dest = self.entity.c["destination"]
        
        # Search for leaves periodically.
        if self.tick_counter % self.leaf_search_period == 0:
            leaf, _ = self.entity.find_closest_entity(self.sight, "leaf")
            if leaf is not None:
                dest.set(leaf)
                return "seeking"
        
        # Let's take care of the energy depleted state.
        energy = self.entity.c["energy"]
        if energy.val < self.energy_depleted*energy.max and self.entity.base.c["energy"].empty == False:
            return "energy depleted"
                
        # Move
        if dest.isvalid == False or dest.arrived:
            # New course.
            self.set_random_destination()
        else:
            # Assume we have a valid destination at this point.
            self.entity.c["velocity"].fullspeedto(dest)
            
        # Increase frame counter.
        self.tick_counter += 1
        
    def entry_actions(self):
        self.tick_counter = 0



class Seeking(BrainState):

    # Allows things to be done not-every frame. Should be reset on enter.
    tick_counter = 0
    
    def __init__(self):
        BrainState.__init__(self, "seeking")

    def process(self, time_passed):
        dest = self.entity.c["destination"]

        if dest.isentity == False:
            return "exploring"
        elif dest.isentity and dest.arrived:
            self.entity.c["inventory"].pickup(dest.val)
            return "delivering"
        else:
            # Head to the leaf.
            self.entity.c["velocity"].fullspeedto(dest)

        self.tick_counter += 1

    def entry_actions(self):
        self.tick_counter = 0


class Delivering(BrainState):
    def __init__(self):
        BrainState.__init__(self, "delivering")
        
    def process(self, time_passed):
        dest = self.entity.c["destination"]
        
        # There shouldn't be any option for this to be anything other than a base.
        if dest.isentity and dest.arrived:
            # Assumes leaf right now.
            self.entity.c["inventory"].give("leaf", dest.val)
            return "exploring"
        else:
            # Head to base.
            self.entity.c["velocity"].fullspeedto(dest)
        
    def entry_actions(self):
        self.entity.c["destination"].set(self.entity.base)



class EnergyDepleted(BrainState):
    def __init__(self):
        BrainState.__init__(self, "energy depleted")
        
    def process(self, time_passed):
        dest = self.entity.c["destination"]
        # TODO: This should be a collision test.
        # Did we make it back to base to eat yet?
        if dest.isentity and dest.arrived:
            # Time to eat.
            return "powering up"
        else:
            self.entity.c["velocity"].fullspeedto(dest)
    
    def entry_actions(self):
        self.entity.c["destination"].set(self.entity.base)
        



class PowerUp(BrainState):
    def __init__(self):
        BrainState.__init__(self, "powering up")
        
    def process(self, time_passed):
        energy = self.entity.c["energy"]
        if energy.val < energy.max:
            energy.val += self.entity.base.remove_resource("energy")

        if energy.val >= energy.max or self.entity.base.c["energy"].empty:
            return "exploring"            
    
    def entry_actions(self):
        self.entity.c["destination"].clear()
        self.entity.c["velocity"].stop()
        
