from entities.components.component import Component



class Inventory(Component):
    """Designates an entity as having an inventory, of being able to be placed
    in an inventory, or both.
    """
    
    _cname = "inventory"
    
    def __init__(self, can_take=True, can_be_taken=False):
        """Constructor.
        
        can_take {bool} Can this entity carry items?
        can_be_taken {bool} Can this entity be carried by another entity?
        """
        self.can_take = can_take
        if can_take:
            # What things are we carrying?
            self.carried = []

        self.can_be_taken = can_be_taken
    
    def can_pickup(self, item):
        """Can we pick up a target entity?
        
        item {Entity} An entity we are attempting to pickup.
        
        return {bool} True if we can, False if not.
        """
        try:
            if (self.can_take and item.c["inventory"].can_be_taken and 
                    (self.entity.body.colliderect(item.body))):
                return True
        except (AttributeError, KeyError):
            pass
        
        # Under all other circumstances, we cannot pick up the entity.
        return False
    
    def pickup(self, item):
        """Attempt to pickup the target entity.
        
        item {Entity} An entity we are attempting to pickup.
        
        return {bool} True if we did pickup the entity, False if not.
        """
        if self.can_pickup(item):
            # This process should probably be refined, but at the moment of
            # writing I'll over comment so I know what to fix later.
            
            # Remove the entity from the world. At the moment, this will likely
            # also prevent the entity from being updated each tick.
            item.world.remove_entity(item)
            
            # Items in an inventory are tagged. This feels a bit wrong.
            item.flags.add("in inventory")
            
            # We assume, if we got here, that we can carry things.
            self.carried.append(item)
            
            return True
        
        # Fail to pickup.
        return False
    
    def give(self, item, whom):
        """Attempt to give an object to some entity.
    
        item {str} Name of an item to give.
        whom {Entity} An entity that we're attempting to give things to.
        
        return {bool} True if the transaction was successful, False if not.
        """
        try:
            if not whom.c["inventory"].can_take:
                return False
        except (AttributeError, KeyError):
            pass

        # Do we even have the item?
        what = None
        for i in self.carried:
            if i.name == item:
                what = i
                break        
        if what is None:
            # Nothing to trade.
            return False
        
        # Are we in contact?
        if not self.entity.body.colliderect(whom.body):
            return False
        
        # We have something to trade, and a target that can accept.
        # Perform the transaction.
        # The item should already be flagged as "in inventory" because it
        # should already have been picked up.
        self.carried.remove(what)
        whom.c["inventory"].carried.append(what)
        return True

        