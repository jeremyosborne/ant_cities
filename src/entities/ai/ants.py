from random import randint
from pymunk.vec2d import Vec2d

from entities.ai.brains import Behavior

class Exploring(Behavior):
    def __init__(self):
        Behavior.__init__(self, "exploring")
        
    def random_destination(self):
        self.entity.destination = Vec2d(randint(0, self.entity.world.width), randint(0, self.entity.world.height))    
 
    def do_actions(self, time_passed):
        #-------------------------------------------------------------------------------------------------------
        #Experimental code for fun.  This section of code can me removed at any time.
        
                #If I see another ant, I change my heading.
        #        close_ant = self.entity.world.get_close_entity(self.entity, "ant", 200)
        #        if close_ant != None:
        #            x, y = close_ant.destination
        #            new_x = y
        #            new_y = x
        #            if new_x > self.entity.world.width: new_x = self.entity.world.width
        #            if new_y > self.entity.world.height: new_y = self.entity.world.height
        #            self.entity.destination = Vec2d(new_x, new_y)
                    
        #End experimental code for fun
        #-------------------------------------------------------------------------------------------------------            
        if randint(1, 200) == 1:
            self.random_destination()
            
    def check_conditions(self):
        leaf = self.entity.world.get_close_entity(self.entity, "leaf", 100)        
        if leaf is not None:
            self.entity.leaf_id = leaf.id
            return "seeking"        
        
        #Let's take care of the energy depleted state
        if self.entity.energy_current < .25 * self.entity.max_energy:
            return "energy depleted"
        
        return None
    
    def entry_actions(self):
        self.entity.speed += 1.
        self.random_destination()
        


class Seeking(Behavior):
    def __init__(self):
        Behavior.__init__(self, "seeking")
        self.leaf_id = None

    def check_conditions(self):
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



class Delivering(Behavior):
    def __init__(self):
        Behavior.__init__(self, "delivering")
        
    #Question for Jeremy start position    
    def check_conditions(self):
        if self.entity.base.location.get_distance(self.entity.location) < self.entity.base.size:
            self.entity.drop(self.entity.world)  # Removes leaf.
            return "exploring"
            
        return None
        
    def entry_actions(self):
        self.entity.destination = self.entity.base.location



class EnergyDepleted(Behavior):
    def __init__(self):
        Behavior.__init__(self, "energy depleted")
        
    def check_conditions(self):
        #Did we make it back to base to eat yet?        
        if self.entity.base.location.get_distance(self.entity.location) < self.entity.base.location:
            # Time to eat.
            return "powering up"            
        return None
        
    def entry_actions(self):
        self.entity.destination = self.entity.base.location



class PowerUp(Behavior):
    def __init__(self):
        Behavior.__init__(self, "powering up")
        
    def do_actions(self, time_passed):
        if self.entity.energy_current < self.entity.max_energy:
            #Only powerup if energy is available.
            if self.entity.base.energy_units > 0:
                self.entity.energy_current += self.entity.energy_recharge_per_second*time_passed
                self.entity.base.energy_units -= self.entity.energy_recharge_to_energy_conversion_ratio*time_passed
           
    def check_conditions(self):
        #Have we fully powered up?        
        if self.entity.energy_current >= self.entity.max_energy:
            return "exploring"            
        return None
    
    def entry_actions(self):
        self.entity.speed = 0.
