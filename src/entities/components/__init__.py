"""Components for managing game entities.

Exports self as a convenience reference to all modules in 
package.

Assumes that any module in this directory (excluding this module) will export
classes within their module structure and all classes should be made available
to the public.

WARNING: This package performs a bit of black magic. Follow the code before
modifying the directory structure.
"""

import os
from inspect import isclass

# Here we do want to do a relative import.
from component import Component


# A cache of the actual component subclasses, not their modules.
# Keyed by component name; value is the component class.
_components_cache = {}

# Modules we don't want to load.
exceptions = set(["__init__", "component"])



def get_component(cname):
    """Retrieve a component class.
    
    Entities wishing to use components should call this function.
    
    If the component is not yet loaded, the component is loaded.
    
    cname {str} The common name of the component.
    """
    if cname in _components_cache:
        return _components_cache[cname]
    # What the name of the module should be.
    elif cname not in exceptions:
        # Due to directory structure, we should load from package and alias.
        component_mod = __import__(".".join([__package__, cname]), fromlist=[cname])
        for item in dir(component_mod):
            item = component_mod.__dict__[item]            
            # Ugh... this is... can't even say how awful this is.
            if isclass(item) and \
                issubclass(item, Component) and \
                item._cname != None and \
                item._cname not in _components_cache:
                _components_cache[item._cname] = item
        return _components_cache[cname]
    else:
        raise ValueError("%s cannot be loaded for some reason")

    