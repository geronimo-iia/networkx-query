import pytest

from networkx_query.operator import lookup_path


def test_lookup_path_default():
    with pytest.raises(RuntimeError):
        lookup_path(True, None)


def test_lookup_path():
    node = {"a": {"b": 1, "c": {"d": "test"}}, "e": False, "d": None}

    assert lookup_path(None, None) == (False, None)
    assert lookup_path(None, "a") == (False, None)
    assert lookup_path(node, None) == (False, None)
    assert lookup_path(node, "e") == (True, False)
    assert lookup_path(node, ()) == (False, None)
    assert lookup_path(node, ("e",)) == (True, False)
    assert lookup_path(node, ("a", "b")) == (True, 1)
    assert lookup_path(node, ("a", "c", "d")) == (True, "test")
    assert lookup_path(node, ("a", "d", "c", "d")) == (False, None)
    assert lookup_path(node, "d") == (True, None)
