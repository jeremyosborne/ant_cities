from random import randint
from pymunk.vec2d import Vec2d

from entities.ai.brains import Behavior

class AntStateExploring(Behavior):
    def __init__(self, ant):
        Behavior.__init__(self, "exploring")
        self.ant = ant
        
    def random_destination(self):
        self.ant.destination = Vec2d(randint(0, self.ant.world.width), randint(0, self.ant.world.height))    
 
    def do_actions(self, time_passed):
        #-------------------------------------------------------------------------------------------------------
        #Experimental code for fun.  This section of code can me removed at any time.
        
                #If I see another ant, I change my heading.
        #        close_ant = self.ant.world.get_close_entity(self.ant, "ant", 200)
        #        if close_ant != None:
        #            x, y = close_ant.destination
        #            new_x = y
        #            new_y = x
        #            if new_x > self.ant.world.width: new_x = self.ant.world.width
        #            if new_y > self.ant.world.height: new_y = self.ant.world.height
        #            self.ant.destination = Vec2d(new_x, new_y)
                    
        #End experimental code for fun
        #-------------------------------------------------------------------------------------------------------            
        if randint(1, 200) == 1:
            self.random_destination()
            
    def check_conditions(self):
        leaf = self.ant.world.get_close_entity(self.ant, "leaf", 100)        
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"        
        
        #Let's take care of the energy depleted state
        if self.ant.energy_current < .25 * self.ant.max_energy:
            return "energy depleted"
        
        return None
    
    def entry_actions(self):
        self.ant.speed += 1.
        self.random_destination()
        


class AntStateSeeking(Behavior):
    def __init__(self, ant):
        Behavior.__init__(self, "seeking")
        self.ant = ant
        self.leaf_id = None

    def check_conditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return "exploring"
        
        if self.ant.location.get_distance(leaf.location) < 2.0:
            self.ant.carry(leaf)
            return "delivering"
        
        return None
    
    def entry_actions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:                        
            self.ant.destination = leaf.location



class AntStateDelivering(Behavior):
    def __init__(self, ant):
        Behavior.__init__(self, "delivering")
        self.ant = ant
        
    #Question for Jeremy start position    
    def check_conditions(self):
        if self.ant.base.location.get_distance(self.ant.location) < self.ant.base.size:
            self.ant.drop(self.ant.world)  # Removes leaf.
            return "exploring"
            
        return None
        
    def entry_actions(self):
        self.ant.destination = self.ant.base.location



class AntStateEnergyDepleted(Behavior):
    def __init__(self, ant):
        Behavior.__init__(self, "energy depleted")
        self.ant = ant
        
    def check_conditions(self):
        #Did we make it back to base to eat yet?        
        if self.ant.base.location.get_distance(self.ant.location) < self.ant.base.location:
            # Time to eat.
            return "powering up"            
        return None
        
    def entry_actions(self):
        self.ant.destination = self.ant.base.location



class AntStatePowerUp(Behavior):
    def __init__(self, ant):
        Behavior.__init__(self, "powering up")
        self.ant = ant
        
    def do_actions(self, time_passed):
        if self.ant.energy_current < self.ant.max_energy:
            #Only powerup if energy is available.
            if self.ant.base.energy_units > 0:
                self.ant.energy_current += self.ant.energy_recharge_per_second*time_passed
                self.ant.base.energy_units -= self.ant.energy_recharge_to_energy_conversion_ratio*time_passed
           
    def check_conditions(self):
        #Have we fully powered up?        
        if self.ant.energy_current >= self.ant.max_energy:
            return "exploring"            
        return None
    
    def entry_actions(self):
        self.ant.speed = 0.
