from itertools import chain
from typing import Dict, Iterable, List, NamedTuple, Optional, Tuple

from networkx import Graph

from .query import prepare_query, search_edges
from .utils import get_first_item, get_second_item

__all__ = ["search_direct_relationships", "PathCriteria", "search_relationships"]


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


class PathCriteria(NamedTuple):
    """Defines path criteria.

    Note:
        With `target={}, egde=...` you could wrote a criteria based on egde constraint only.

    Args:
        target (Dict): target node query constraint.
            `{}` means all nodes
        edge (Dict): optional edge query constraint
    """

    target: Dict
    edge: Optional[Dict] = None


def search_relationships(graph: Graph, source: Dict, *nodes: PathCriteria) -> Iterable[List]:
    """Search all valid path according specified template.

    Args:
        graph (Graph): graph instance
        source (Dict): source node query constraint
        nodes (PathCriteria): ordered list of path criteria

    Returns:
        (Iterable[Tuple]): all path which validate specification

    Raises:
        (RuntimeError): if a path criteria have no constraint
    """

    if not nodes:
        # cast single edge to path
        for a, b in search_direct_relationships(graph=graph, source=source):
            yield [a, b]
        return

    # Validate path template
    node_count = len(nodes)
    assert node_count >= 1

    # build pair of relations ships
    relationships = []

    for i in range(node_count):
        item = set(
            search_direct_relationships(
                graph=graph,
                source=source if i == 0 else nodes[i - 1].target,
                edge=nodes[i].edge,
                target=nodes[i].target,
            )
        )
        relationships.append(item)

        if not len(item):
            raise RuntimeError(f"No valid path from {i}th criteria.")

    # recursive
    def visit(path, node, i):
        for a, b in filter(lambda t: t[0] == node, relationships[i]):
            if i + 1 < node_count:
                yield from visit(path=path + [a], node=b, i=i + 1)
            else:
                yield path + [a, b]

    for a, b in relationships[0]:
        if node_count == 1:
            yield [a, b]
        else:
            yield from visit(path=[a], node=b, i=1)


def join_relationship(
    graph: Graph, source: Iterable[Tuple], target: Iterable[Tuple]
) -> Iterable[Tuple]:  # pragma: no cover
    """Join two relation ship.

    With  source = (a, b), target = (c, d)
    return (e, _) as e in source (e, b) and e in target( e, d)

    """

    _source = set(source)
    _target = set(target)

    _nodes = set(filter(get_first_item, _source)).intersection(set(filter(get_first_item, _target)))

    return chain(
        filter(lambda edge: get_first_item(edge) in _nodes, _source),
        filter(lambda edge: get_first_item(edge) in _nodes, _target),
    )


def chain_relationship(
    graph: Graph, source: Iterable[Tuple], target: Iterable[Tuple]
) -> Iterable[Tuple]:  # pragma: no cover
    """Chain two direct relation ship.

    return edge (_ e) or (e, _) as e in source(_, e) and e in target (e, _)

    """

    _source = set(source)
    _target = set(target)

    _nodes = set(filter(get_second_item, _source)).intersection(set(filter(get_first_item, _target)))

    return chain(
        filter(lambda edge: get_second_item(edge) in _nodes, _source),
        filter(lambda edge: get_first_item(edge) in _nodes, _target),
    )
