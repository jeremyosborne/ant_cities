"""Basic component system.

Components are units that represent common building blocks -- health, energy, 
magic power, attributes, status effects, etc. -- of an entity. A spider might
have health like an ant, but a spider might have more health. A leaf might
have no health, but might make use of the energy component to represent
how nutritious it is.

EXPERIMENTAL: Components are created as instances within an Entity and added
to a component dict via name and add interface.
"""


class Component(object):
    """Components are an opt in interface.
    """
    
    # {str} Required: components must all have a unique name.
    _cname = None
    
    # {Entity} Components receive a pointer to their owner entity when they are added.
    entity = None
    
    # Should components be added to process loop? This attribute should be set
    # once on class construction and treated as read only.
    doprocess = True
    
    # Components can have their own init, but the Component does not provide
    # any recipe.
    
    def process(self, time_passed):
        """Called every round to perform rudimentary updates to the component.
        
        By default, components do not process.
        
        time_passed {float} Delta number of seconds since the last time this
        function was called.
        """
        pass
    
    def destroy(self):
        """As part of the entity/component contract, this will be called when
        the componet should no longer be used and has been removed from an
        entity.
        """
        self.entity = None
