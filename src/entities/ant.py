from entities.entity import Entity
import entities.ai.ants as antbrainstates

class Ant(Entity):
    
    name = "ant"
    
    def __init__(self, world, base):
        
        Entity.__init__(self, world)
                
        self.brain.add_state(antbrainstates.Exploring())
        self.brain.add_state(antbrainstates.Seeking())
        self.brain.add_state(antbrainstates.Delivering())
        self.brain.add_state(antbrainstates.EnergyDepleted())
        self.brain.add_state(antbrainstates.PowerUp())
        # Default state.
        self.brain.set_state("exploring")
        
        self.c.add("health")
        self.c.add("energy", burn_rate=2.)
        
        self.c.add("facing")
        self.c.add("velocity", max_speed=120., acceleration=30., rotation_speed=180.)
        self.c.add("destination")
        self.c.add("inventory")

        # {Entity} What is our home base.
        self.base = base
        
    @property
    def team_id(self):
        """What team are we on?
        """
        return self.base.c["team"].id
        
    def process(self, time_passed):
        Entity.process(self, time_passed)

        energy = self.c["energy"]
        health = self.c["health"]
        
        # Is ant energy so low that we need to dump health into energy?
        if energy.empty:
            energy.val += 100
            health.val -= 10
        
        # Heading matches course of velocity.
        self.c["facing"].set(self.c["velocity"].course)
        
        # Should the ant die?
        if health.dead:
            self.flags.add("dead")
    
