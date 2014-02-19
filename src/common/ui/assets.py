"""Asset loaders and asset caches.
"""
import os

class AssetCache(object):
    """A loader and cache for static resources.
    """
    def __init__(self, basepath=".", loader=None, copier=None):
        """Constructor.
        
        basepath {string} Base path from which to load all assets.
        loader {function} A function that takes a path and returns an asset
        object to be cached. Defaults to class implemented method.
        copier {function} A function that takes an asset object and returns a
        copy. Defaults to class implemented method.
        """
        self.basepath = basepath
        # Single layer cache used to store static assets.
        self._cache = {}
        
        if callable(loader):
            self._loader = loader

        if callable(copier):
            self._copier = copier

    def _loader(self, path):
        """Implemented in init to allow loading of assets.
        
        Used to perform the loading of assets from disk.
        
        path {str} Absolute path to load an asset from.
        
        return {mixed} an asset.
        """
        raise NotImplementedError("Must override this method.")
    
    def _copier(self, asset):
        """Implemented in init to allow copying of assets.
        
        Used to copy an asset when a copy is requested.
        
        asset {mixed} The asset that will be copied.
        """
        raise NotImplementedError("Must override this method.")

    def path_translator(self, name):
        """Translate a resource name into something loadable.
        
        By default, a name is simply appended to the basepath and then loading
        is attempted.
        
        returns a string.
        """
        return os.path.join(self.basepath, name)

    def count_cache(self):
        """How many assets are currently cached.
        """
        return len(self._cache)

    def load(self, name):
        """Load a resource and store it in the cache.
        
        Will reload an existing resource.
        
        name {str} Resource to load.
        
        returns the resource as a convenience.
        """
        self._cache[name] = self._loader(self.path_translator(name))
        return self._cache[name]
    
    def get(self, name):
        """Get a copy of a resource from the cache. 
        
        As a convenience, load the image if not yet loaded.
        
        name {str} The name of the asset to retrieve.
        
        return {object} copy of the cached resource.
        """
        return self._copier(self.get_ref(name))

    def get_ref(self, name):
        """Get a reference of a resource from the cache.
        
        As a convenience, load the image if not yet loaded.

        name {str} The name of the asset to retrieve.
        
        return {object} the cached resource.
        """
        if name in self._cache:
            return self._cache[name]
        else:
            return self.load(name)

    def delete(self, name):
        """Delete a particular resource from the cache.
        
        returns {bool} True if something was actually deleted from the cache,
        False if not.
        """
        try:
            del self._cache[name]
            return True
        except KeyError:
            # Fail if nothing in the cache by that name.
            return False

    def delete_all(self):
        """Delete all items from the cache.
        """
        self._cache = {}
