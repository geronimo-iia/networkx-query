import pytest

from networkx_query.operator import lookup_path


def test_lookup_path_default():
    with pytest.raises(RuntimeError):
        lookup_path(True, None)


def test_lookup_path():

    node = {'a': {'b': 1, 'c': {"d": "test"}}, 'e': False, 'd': None}

    assert (False, None) == lookup_path(None, None)
    assert (False, None) == lookup_path(None, "a")
    assert (False, None) == lookup_path(node, None)
    assert (True, False) == lookup_path(node, "e")
    assert (False, None) == lookup_path(node, ())
    assert (True, False) == lookup_path(node, ("e",))
    assert (True, 1) == lookup_path(node, ("a", "b"))
    assert (True, "test") == lookup_path(node, ("a", "c", "d"))
    assert (False, None) == lookup_path(node, ("a", "d", "c", "d"))
    assert (True, None) == lookup_path(node, "d")
