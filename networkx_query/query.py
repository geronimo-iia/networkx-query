"""networkx-query public interace definition."""
from typing import Any, Dict, Iterable, Tuple

from networkx import Graph

from .definition import Evaluator, ParserException
from .parser import compile_ast, parse

__all__ = ['search_nodes', 'search_edges', 'prepare_query', 'ParserException']


def prepare_query(query: Dict) -> Evaluator:
    """Transform expression query as a function.

    Arguments:
        query (Dict): expression query as dictionary

    Returns:
        (Evaluator): evaluator function

    Exceptions:
        (ParserException): if a parse error occurs

    """
    return compile_ast(parse(expra=query))


def search_nodes(graph: Graph, query: Dict) -> Iterable[Any]:
    """Search nodes in specified grapg which match query.

    Arguments:
        graph (Graph): networkx graph instance
        query (Dict): query expression

    Returns:
        (Iterable[Any]): results as an iterable of node identifier.

    Exceptions:
        (ParserException): if a parse error occurs

    """
    _predicate = prepare_query(query)

    return map(
        lambda n: n[0], filter(lambda n: n[1], map(lambda node: (node[0], _predicate(node[1])), graph.nodes(data=True)))
    )


def search_edges(graph: Graph, query: Dict) -> Iterable[Tuple]:
    """Search edges in specified grapg which match query.

    Arguments:
        graph (Graph): networkx graph instance
        query (Dict): query expression

    Returns:
        (Iterable[Tuple]): results as an iterable of edge identifier (tuple).

    Exceptions:
        (ParserException): if a parse error occurs

    """
    _predicate = prepare_query(query)
    return map(
        lambda n: n[0],
        filter(lambda n: n[1], map(lambda edge: ((edge[0], edge[1]), _predicate(edge[2])), graph.edges(data=True))),
    )
