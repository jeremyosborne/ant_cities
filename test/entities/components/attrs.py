from src.entities.components.attrs import Attrs

def test_attrs():
    a = Attrs()
    
    a.create("health", 50, 100, 0)
    
    assert "health" in a, "Found attribute."
    assert a["health"] == 50, "Correct value."
    assert a.get("health").max == 100, "Correct max value."
    assert a.get("health").min == 0, "Correct min value."
    assert a.delta("health", -100) == -50, "Correct delta value."
    assert a.delta("health", -100) == 0, "Correct delta value."
    a["health"] = 200
    assert a["health"] == 100, "Correct max value health."
     
    