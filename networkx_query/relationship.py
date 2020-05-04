from itertools import chain
from typing import Dict, Iterable, Optional, Tuple

from networkx import Graph

from .query import prepare_query, search_edges
from .utils import get_first_item, get_second_item

__all__ = ["search_direct_relationships", "join_relationship"]


def search_direct_relationships(
    graph: Graph, source: Optional[Dict] = None, edge: Optional[Dict] = None, target: Optional[Dict] = None
) -> Iterable[Tuple]:
    """Search direct relation ship.

    Arguments:
        graph (Graph): graph instance
        source (Optional[Dict]): optional source node query constraint
        edge (Optional[Dict]): optional edge query constraint
        target (Optional[Dict]): optional target node query constraint

    Returns:
        (Iterable[Tuple]): itrable tuple of edge

    """
    _iterable = search_edges(graph=graph, query=edge) if edge else graph.edges()

    if source:
        _predicate_source = prepare_query(source)
        _iterable = filter(lambda edge: _predicate_source(graph.nodes[edge[0]]), _iterable)

    if target:
        _predicate_target = prepare_query(target)
        _iterable = filter(lambda edge: _predicate_target(graph.nodes[edge[1]]), _iterable)

    return _iterable


def join_relationship(
    graph: Graph, source: Iterable[Tuple], target: Iterable[Tuple], join_on_source_origin: Optional[bool] = True
) -> Iterable[Tuple]:  # pragma: no cover
    """Join two relation ship.

    With  source = (a, b), target = (c, d)
    If join_on_source_origin is set, return (e, f) as e in source(e, _) and e in target(e, _)
    else return edge (e, _) or (_ e) as e in source(_, e) and e in target(e, _)
    """

    _source = set(source)
    _target = set(target)

    _source_filter = get_first_item if join_on_source_origin else get_second_item

    _nodes = set(filter(_source_filter, _source)).intersection(set(filter(get_first_item, _target)))

    return chain(
        filter(lambda edge: _source_filter(edge) in _nodes, _source),
        filter(lambda edge: get_first_item(edge) in _nodes, _target),
    )
