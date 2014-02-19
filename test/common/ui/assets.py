import os
from src.common.ui.assets import AssetCache

def test_assets_assetcache_defaults():
    a = AssetCache(basepath="yourmom")
    
    assert a.basepath == "yourmom"
    
    err = None
    try:
        a.load("test")
    except NotImplementedError as err:
        pass
    assert err, "We got an error."

    err = None
    try:
        a.get("test")
    except NotImplementedError as err:
        pass
    assert err, "We got an error."

    err = None
    try:
        a.get_ref("test")
    except NotImplementedError as err:
        pass
    assert err, "We got an error."



def test_assets_assetcache_load():
    difficult_to_count_tests = {
                                "counted": 0,
                                "expected": 1
                                }
    bpath = "your mom"
    asset_name = "cats"
    def mock_loader(path):
        # Make sure we're getting a transformed path.
        assert path == os.path.join(bpath, asset_name), "Received expected path."
        difficult_to_count_tests["counted"] += 1
        
        return {"src": path}
    
    a = AssetCache(basepath=bpath, loader=mock_loader)
    test_asset = a.load(asset_name)
    assert test_asset == {"src": os.path.join(bpath, asset_name)}, "Got expected object."
    
    # Confirm the number of tests we can't normally confirm
    assert difficult_to_count_tests["counted"] == difficult_to_count_tests["expected"]



def test_assets_assetcache_get():
    bpath = "your mom"
    asset_name = "cats"
    
    def mock_loader(path):
        return {"src": path}
    
    def mock_copier(o):
        return o.copy()
    
    a = AssetCache(basepath=bpath, loader=mock_loader, copier=mock_copier)
    test_asset = a.load(asset_name)
    copied_asset = a.get(asset_name)
    assert test_asset == copied_asset, "Got expected copy of object."
    assert id(test_asset) != id(copied_asset), "Object is not the same object."


def test_assets_assetcache_get_ref():
    bpath = "your mom"
    asset_name = "cats"
    def mock_loader(path):
        return {"src": path}
    
    a = AssetCache(basepath=bpath, loader=mock_loader)
    test_asset = a.load(asset_name)
    assert id(test_asset) == id(a.get_ref(asset_name)), "Returned the same object."


    
def test_assets_assetcache_delete():
    bpath = "your mom"
    asset_name = "cats"
    def mock_loader(path):
        return {"src": path}
    
    a = AssetCache(basepath=bpath, loader=mock_loader)
    a.load(asset_name)
    assert a.count_cache() == 1, "Expected number in cache."
    a.delete(asset_name)
    assert a.count_cache() == 0, "Expected number in cache."



def test_assets_assetcache_delete_all():
    def mock_loader(path):
        return {"src": path}
    
    a = AssetCache(basepath="..", loader=mock_loader)
    a.load("test")
    a.load("test2")
    a.load("test3")
    assert a.count_cache() == 3, "Expected number in cache."
    a.delete_all()
    assert a.count_cache() == 0, "Expected number in cache."

