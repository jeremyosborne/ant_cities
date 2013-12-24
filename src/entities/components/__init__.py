"""Components for managing game entities.

Exports self as a convenience reference to all modules in 
package.

Assumes that any module in this directory (excluding this module) will export
classes within their module structure and all classes should be made available
to the public.

WARNING: THIS PACKAGE PERFORMS BLACK MAGIC.
"""

_components_cached = False

def initialize():
    """Load all of the component classes into this package reference.
    """
    global _components_cached

    import os
    import fnmatch
    import sys
    import inspect

    if _components_cached == True:
        return
    # else, attempt to load modules once and only once.
    _components_cached = True
    # Modules we don't want to load.
    exceptions = set(["__init__.py", "component.py"])
    # Reference to this module, give us access to __dict__.
    module_self = sys.modules[__name__]
    # Only a single level (for now).
    for f in os.listdir(os.path.dirname(__file__)):
        if fnmatch.fnmatch(f, "*.py") and f not in exceptions:
            # We need to keep the package relative reference. For some
            # reason, this import will not work without it.
            component_mod_name = ".".join([__package__, f[:-3]])
            component_mod = __import__(component_mod_name, fromlist=[f[:-3]])
            for item in dir(component_mod):
                if inspect.isclass(component_mod.__dict__[item]):
                    # Assume that if it's a class, we want it attached to us.
                    setattr(module_self, item, component_mod.__dict__[item])

# Run on first time through.
initialize()
