from random import randint
from entities.ai.brains import BrainState

class Exploring(BrainState):
    
    # What is close_enough to our destination when randomly exploring.
    close_enough = 100.
        
    # At what percentage will we attempt to go get energy.
    energy_depleted = .25
    
    # How many ticks between when we search for leaves?
    leaf_search_period = 17

    # What is the search radius for finding things?
    sight = 500.
    
    def __init__(self):
        BrainState.__init__(self, "exploring")
        
        # Allows things to be done not-every frame.
        # Should be reset on enter. This is just a place holder.
        self.tick_counter = 0
        
    def set_random_destination(self):
        p = (randint(0, self.entity.world.width), randint(0, self.entity.world.height))
        self.entity.c["destination"].set(p)
        
    def process(self, time_passed):
        # Requires a destination component
        destination = self.entity.c["destination"]
        
        # Search for leaves periodically.
        if self.tick_counter % self.leaf_search_period == 0:
            leaf, _ = self.entity.find_closest_entity(self.sight, "leaf")
            if leaf is not None:
                destination.set(leaf)
                return "seeking"
        
        # Let's take care of the energy depleted state.
        energy = self.entity.c["energy"]
        if energy.val < self.energy_depleted*energy.max and self.entity.base.c["energy"].empty == False:
            return "energy depleted"
                
        # Move
        v = self.entity.c["velocity"]
        if destination.isvalid == False or destination.distanceto < self.close_enough:
            # New course.
            self.set_random_destination()
        else:
            # Assume we have a valid destionation at this point.
            v.fullspeedto(destination)
            
        # Increase frame counter.
        self.tick_counter += 1
        
    def entry_actions(self):
        self.tick_counter = 0



class Seeking(BrainState):
    
    # How close do we have to be to get the leaf?
    close_enough = 2.0
    
    def __init__(self):
        BrainState.__init__(self, "seeking")

        # Should be reset on enter. This is just a place holder.
        self.tick_counter = 0

    def process(self, time_passed):
        destination = self.entity.c["destination"]
        v = self.entity.c["velocity"]

        if destination.isentity == False:
            return "exploring"
        elif destination.distanceto < self.close_enough:
            self.entity.carry(destination.val)
            return "delivering"
        else:
            # Head to the leaf.
            v.fullspeedto(destination)

        self.tick_counter += 1

    def entry_actions(self):
        self.tick_counter = 0


class Delivering(BrainState):
    def __init__(self):
        BrainState.__init__(self, "delivering")
        
    def process(self, time_passed):
        destination = self.entity.c["destination"]
        v = self.entity.c["velocity"]
        
        # TODO: This should be a collision test.
        if destination.distanceto < self.entity.base.size:
            # Assumes leaf right now.
            self.entity.drop()
            return "exploring"
        else:
            # Head to base.
            v.fullspeedto(destination)
        
    def entry_actions(self):
        self.entity.c["destination"].set(self.entity.base)



class EnergyDepleted(BrainState):
    def __init__(self):
        BrainState.__init__(self, "energy depleted")
        
    def process(self, time_passed):
        destination = self.entity.c["destination"]
        v = self.entity.c["velocity"]
        # TODO: This should be a collision test.
        # Did we make it back to base to eat yet?
        if destination.distanceto < self.entity.base.size:
            # Time to eat.
            return "powering up"
        else:
            v.fullspeedto(destination)
    
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
        
