"""Utilities with networkx."""

from typing import Any, Callable, Iterable, List, Tuple

from networkx import DiGraph, Graph, all_simple_paths
from networkx.utils import pairwise

__all__ = [
    "get_first_item",
    "get_second_item",
    "get_two_first_items",
    "filter_by_degree",
    "get_attributs",
    'search_root_nodes',
    'search_leaf_nodes',
    'search_simple_path',
]


def get_first_item(t: Tuple) -> Any:
    """Returns first item of tuple."""
    return t[0]


def get_second_item(t: Tuple) -> Any:  # pragma: no cover
    """Returns second item of tuple."""
    return t[1]


def get_two_first_items(t: Tuple) -> Tuple:
    """Return (first, second) item of tuple as tuple."""
    return (t[0], t[1])


def filter_by_degree(degree: int) -> Callable[[Any], bool]:  # pragma: no cover
    """Generate a filter for specified degree."""

    def _filter(node: Any) -> bool:
        (id, d) = node
        return d == degree

    return _filter


def get_attributs(*names: str) -> Callable[[Tuple], List]:  # pragma: no cover
    """Returns attributs list for specified node or edge."""

    def _map(t: Tuple) -> List:
        (v, d) = t
        return [d[name] for name in names]

    return _map


def search_root_nodes(graph: DiGraph) -> Iterable[Any]:  # pragma: no cover
    """Search nodes with no 'in' edges.

    Arguments:
        graph (DiGraph): networkx digraph instance

    Returns:
        (Iterable[Any]): results as an iterable of node identifier.

    """
    return map(get_first_item, filter(filter_by_degree(0), graph.in_degree()))


def search_leaf_nodes(graph: DiGraph) -> Iterable[Any]:  # pragma: no cover
    """Search nodes with no 'out' edges.

    Arguments:
        graph (DiGraph): networkx digraph instance

    Returns:
        (Iterable[Any]): results as an iterable of node identifier.

    """
    return map(get_first_item, filter(filter_by_degree(0), graph.out_degree()))


def search_simple_path(graph: Graph, source: Any, target: Any, cutoff=None):  # pragma: no cover
    """Returns a list of edges."""
    return map(pairwise, all_simple_paths(graph, source=target, target=target, cutoff=cutoff))
