"""Team information.

This should become a management abstract object and not a component.
"""

from entities.components.component import Component

class Team(Component):
    """Information about the team this entity belongs to.
    
    If the entity has no team, they shouldn't have a team component.
    """
    
    _cname = "team"
    
    doprocess = False
    
    def __init__(self, id, name):
        """Setup team statistics.
        
        id {mixed} Unique identifer of this team (unique among all teams).
        name {str} Human friendly team name.
        """
        self.id = id
        self.name = name

    def __str__(self):
        return "Team (%s): %s" % (self.id, self.name)
