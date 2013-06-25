import entities
import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

import global_data

class State(object):
    
    def __init__(self, name):        
        self.name = name
        
    def do_actions(self):
        pass
        
    def check_conditions(self):        
        pass    
    
    def entry_actions(self):        
        pass    
    
    def exit_actions(self):        
        pass
    
class StateMachine(object):
    
    def __init__(self):
        
        self.states = {}
        self.active_state = None
    
    
    def add_state(self, state):
        
        self.states[state.name] = state
        
        
    def think(self):
        
        if self.active_state is None:
            return
        
        self.active_state.do_actions()        

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    
    def set_state(self, new_state_name):
        
        if self.active_state is not None:
            self.active_state.exit_actions()
            
        self.active_state = self.states[new_state_name]        
        self.active_state.entry_actions()
        
     
class AntStateExploring(State):
    
    def __init__(self, ant):
        
        State.__init__(self, "exploring")
        self.ant = ant
        
    def random_destination(self):
        
        self.ant.destination = Vector2(randint(0, self.ant.world.width), randint(0, self.ant.world.height))    
    
    def do_actions(self):
        
        if randint(1, 20) == 1:
            self.random_destination()
            
    def check_conditions(self):
                        
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)        
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"        
        
        #Let's take care of the hungry state
        if self.ant.hunger < 0:
            return "hungry"
        
        return None
    
    def entry_actions(self):
        
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()
        
        
class AntStateSeeking(State):
    
    def __init__(self, ant):
        
        State.__init__(self, "seeking")
        self.ant = ant
        self.leaf_id = None
    
    def check_conditions(self):
        
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return "exploring"
        
        if self.ant.location.get_distance_to(leaf.location) < 5.0:
        
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)  #Removing leaf from the world
            return "delivering"
        
        return None
    
    def entry_actions(self):
    
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:                        
            self.ant.destination = leaf.location
            self.ant.speed = 160. + randint(-20, 20)
        
        
class AntStateDelivering(State):
    
    def __init__(self, ant):
        
        State.__init__(self, "delivering")
        self.ant = ant
        
        
    def check_conditions(self):
                
        if Vector2(*self.ant.base_location).get_distance_to(self.ant.location) < global_data.NEST_SIZE:
            self.ant.drop(self.ant.world)  # Drops leaf onto the background frame.
            return "exploring"
            
        return None
        
        
    def entry_actions(self):
        
        self.ant.speed = 60.        
        #random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*self.ant.base_location) # + random_offset       
       
class AntStateHungry(State):
    
    def __init__(self, ant):
        
        State.__init__(self, "hungry")
        self.ant = ant
        
        
    def check_conditions(self):
        
        #Did we make it back to base to eat yet?        
        if Vector2(*self.ant.base_location).get_distance_to(self.ant.location) < global_data.NEST_SIZE:
            # Time to eat.
            return "eating"            
        return None
        
        
    def entry_actions(self):
        
        self.ant.speed = 60.        
        #random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*self.ant.base_location) # + random_offset

class AntStateEating(State):
    
    def __init__(self, ant):
        
        State.__init__(self, "eating")
        self.ant = ant
        
        
    def check_conditions(self):
        
        #Have we eaten our fill?        
        if self.ant.hunger < 1000:
            self.ant.hunger += 100
            self.ant.base.food_units -= 0.01
        else:
            return "exploring"            
        return None
        
        
    def entry_actions(self):
        
        self.ant.speed = 0.        
        #random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        #self.ant.destination = Vector2(*self.ant.base_location) # + random_offset
        
