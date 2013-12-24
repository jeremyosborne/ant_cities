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
import inspect

# Here we do want to do a relative import.
from component import Component


# A cache of the actual component subclasses, not their modules.
# Keyed by component name; value is the component class.
_components_cache = {}

# Modules we don't want to load.
exceptions = set(["__init__", "component"])



def get_component(name):
    """Retrieve a component class.
    
    Entities wishing to use components should call this function.
    
    If the component is not yet loaded, the component is loaded.
    
    name {str} The common name of the component.
    """
    if name in _components_cache:
        return _components_cache[name]
    # What the name of the module should be.
    elif name not in exceptions:
        component_mod = __import__(".".join([__package__, name]), fromlist=[name])
        for item in dir(component_mod):
            item = component_mod.__dict__[item]
            # Sanity checking.
            if issubclass(Component, item) and item not in _components_cache:
                _components_cache[item.name] = item
            # Load until we get the component we want.
            if name == item.name:
                return item
    else:
        raise ValueError("%s cannot be loaded for some reason")

    