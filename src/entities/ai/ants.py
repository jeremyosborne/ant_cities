from random import randint
from commonmath import courseto
from entities.ai.brains import BrainState

class Exploring(BrainState):
    
    # What is close_enough to our destination when randomly exploring.
    close_enough = 100.
    
    # What is the search radius for finding leaves?
    leaf_in_eyesight = 200.
    
    # At what percentage will we attempt to go get energy.
    energy_depleted = .25
    
    def __init__(self):
        BrainState.__init__(self, "exploring")
        
    def set_random_destination(self):
        p = (randint(0, self.entity.world.width), randint(0, self.entity.world.height))
        self.entity.components["destination"].set(p)
 
    def process(self, time_passed):
        # Requires a destination component
        destination = self.entity.components["destination"]
        
        # We wants leaves.
        leaf, _ = self.entity.find_closest_entity(self.leaf_in_eyesight, "leaf")        
        if leaf is not None:
            destination.set(leaf)
            return "seeking"        
        
        # Let's take care of the energy depleted state.
        energy = self.entity.components["energy"]
        if energy.current < self.energy_depleted*energy.max:
            return "energy depleted"
        
        # Move
        ve = self.entity.components["velocityengine"]
        if not destination.isvalid or destination.distanceto < self.close_enough:
            # New course.
            self.set_random_destination()
        else:
            # Assume we have a valid destionation at this point.
            # TODO: Move this part to the ant process. Brain just makes the
            # decisions.
            ve.fullspeedto(destination.courseto)
        
    def entry_actions(self):
        # Exploring is exploring. Don't come here if you already have a target.
        #self.set_random_destination()
        pass


class Seeking(BrainState):
    
    # How close do we have to be to get the leaf?
    close_enough = 2.0
    
    def __init__(self):
        BrainState.__init__(self, "seeking")

    def process(self, time_passed):
        destination = self.entity.components["destination"]

        if destination.isentity == False:
            return "exploring"
        elif destination.distanceto < self.close_enough:
            self.entity.carry(self.destination.val)
            return "delivering"
        else:
            # TODO: Possible course correction if for some reason we can't
            # reach a leaf.
            pass



class Delivering(BrainState):
    def __init__(self):
        BrainState.__init__(self, "delivering")
        
    def process(self, time_passed):
        destination = self.entity.components["destination"]
        # TODO: This should be a collision test.
        if destination.distanceto < self.entity.base.size:
            # Assumes leaf right now.
            self.entity.drop()
            return "exploring"
        
    def entry_actions(self):
        self.entity.components["destination"].set(self.entity.base)



class EnergyDepleted(BrainState):
    def __init__(self):
        BrainState.__init__(self, "energy depleted")
        
    def process(self, time_passed):
        destination = self.entity.components["destination"]
        # TODO: This should be a collision test.
        # Did we make it back to base to eat yet?
        if destination.distanceto < self.entity.base.size:
            # Time to eat.
            return "powering up"
    
    def entry_actions(self):
        destination = self.entity.components["destination"]
        ve = self.entity.components["velocityengine"]
        
        destination.set(self.entity.base)
        ve.fullspeedto(destination.courseto)
        



class PowerUp(BrainState):
    def __init__(self):
        BrainState.__init__(self, "powering up")
        
    def process(self, time_passed):
        energy = self.entity.components["energy"]
        if energy.current < energy.max:
            # Only powerup if energy is available.
            if self.entity.base.components["energy"].current > 0:
                # TODO: Get energy from the base. No energy at base, dead ant.
                # Right now, the base will not be drained of energy at all.
                energy.current += 1000*time_passed

        # Have we fully powered up?
        if energy.current >= energy.max:
            return "exploring"            
    
    def entry_actions(self):
        self.entity.components["destination"].clear()
        self.entity.components["velocityengine"].stop()
        
