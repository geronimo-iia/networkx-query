"""networkx-query public interace definition."""

from typing import Any, Dict, Iterable, Tuple

from networkx import Graph

from .parser import prepare_query
from .utils import get_first_item, get_two_first_items

__all__ = ['search_nodes', 'search_edges']


def search_nodes(graph: Graph, query: Dict) -> Iterable[Any]:
    """Search nodes in specified graph which match query.

    Arguments:
        graph (Graph): networkx graph instance
        query (Dict): query expression

    Returns:
        (Iterable[Any]): results as an iterable of node identifier.

    Exceptions:
        (ParserException): if a parse error occurs

    """
    _predicate = prepare_query(query)
    return map(get_first_item, filter(lambda node: _predicate(node[1]), graph.nodes(data=True)))


def search_edges(graph: Graph, query: Dict) -> Iterable[Tuple]:
    """Search edges in specified graph which match query.

    Arguments:
        graph (Graph): networkx graph instance
        query (Dict): query expression

    Returns:
        (Iterable[Tuple]): results as an iterable of edge identifier (tuple).

    Exceptions:
        (ParserException): if a parse error occurs

    """
    _predicate = prepare_query(query)
    return map(get_two_first_items, filter(lambda edge: _predicate(edge[2]), graph.edges(data=True)))
