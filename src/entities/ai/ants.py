from random import randint
from pymunk.vec2d import Vec2d

from entities.ai.brains import BrainState

class Exploring(BrainState):
    def __init__(self):
        BrainState.__init__(self, "exploring")
        
    def random_destination(self):
        self.entity.destination = Vec2d(randint(0, self.entity.world.width), randint(0, self.entity.world.height))    
 
    def process(self, time_passed):
        # We wants leaves.
        leaf = self.entity.world.get_close_entity(self.entity, "leaf", 100)        
        if leaf is not None:
            self.entity.leaf_id = leaf.id
            return "seeking"        
        
        # Let's take care of the energy depleted state.
        energy = self.entity.components["energy"]
        if energy.current < .25*energy.max:
            return "energy depleted"

        # Random walk.
        if randint(1, 200) == 1:
            self.random_destination()
        
        return None
            
    def entry_actions(self):
        self.entity.speed += 1.
        self.random_destination()
        


class Seeking(BrainState):
    def __init__(self):
        BrainState.__init__(self, "seeking")
        self.leaf_id = None

    def process(self, time_passed):
        leaf = self.entity.world.get(self.entity.leaf_id)
        if leaf is None:
            return "exploring"
        
        if self.entity.location.get_distance(leaf.location) < 2.0:
            self.entity.carry(leaf)
            return "delivering"
        
        return None
    
    def entry_actions(self):
        leaf = self.entity.world.get(self.entity.leaf_id)
        if leaf is not None:                        
            self.entity.destination = leaf.location



class Delivering(BrainState):
    def __init__(self):
        BrainState.__init__(self, "delivering")
        
    def process(self, time_passed):
        if self.entity.base.location.get_distance(self.entity.location) < self.entity.base.size:
            self.entity.drop(self.entity.world)  # Removes leaf.
            return "exploring"
            
        return None
        
    def entry_actions(self):
        self.entity.destination = self.entity.base.location



class EnergyDepleted(BrainState):
    def __init__(self):
        BrainState.__init__(self, "energy depleted")
        
    def process(self, time_passed):
        #Did we make it back to base to eat yet?        
        if self.entity.base.location.get_distance(self.entity.location) < self.entity.base.size:
            # Time to eat.
            return "powering up"
        return None
        
    def entry_actions(self):
        self.entity.destination = self.entity.base.location



class PowerUp(BrainState):
    def __init__(self):
        BrainState.__init__(self, "powering up")
        
    def process(self, time_passed):
        energy = self.entity.components["energy"]
        if energy.current < energy.max:
            # Only powerup if energy is available.
            if self.entity.base.energy_units > 0:
                # TODO: Get energy from the base. No energy at base, dead ant.
                energy.current += 1000*time_passed

        # Have we fully powered up?
        if energy.current >= energy.max:
            return "exploring"            
        return None
    
    def entry_actions(self):
        self.entity.speed = 0.
