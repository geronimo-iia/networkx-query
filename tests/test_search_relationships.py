import networkx as nx
import pytest

from networkx_query.relationship import PathCriteria, search_relationships


def build_graph():
    g = nx.DiGraph()
    g.add_node(1, product="a")
    g.add_node(2, product="b")
    g.add_node(3, product="c")
    g.add_node(4, product="d")

    g.add_edge(1, 2)
    g.add_edge(1, 3, weight=2)
    g.add_edge(1, 4)

    g.add_edge(2, 4)
    g.add_edge(3, 4)

    return g


def test_search_relationships_basics():
    g = build_graph()
    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},
        )
    )
    assert result
    assert len(result) == 3
    assert [1, 2] in result
    assert [1, 3] in result
    assert [1, 4] in result

    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},
            PathCriteria(target={"eq": [("product",), "b"]}),
            PathCriteria(target={"eq": [("product",), "d"]}),
        )
    )
    assert result
    assert len(result) == 1
    assert result[0] == [1, 2, 4]

    with pytest.raises(RuntimeError):
        result = list(
            search_relationships(
                g,
                {"eq": [("product",), "d"]},  # node 4
                PathCriteria(target={"eq": [("product",), "a"]}),  # node 1,
                PathCriteria(target={"eq": [("product",), "d"]}),  # node 4
            )
        )


def test_search_relationships_one_node():
    g = build_graph()

    result = list(
        search_relationships(g, {"eq": [("product",), "a"]}, PathCriteria(target={"eq": [("product",), "c"]}))  # node 1
    )  # 3
    assert len(result) == 1
    assert result[0] == [1, 3]

    result = list(
        search_relationships(
            g, {"eq": [("product",), "a"]}, PathCriteria(target={}, edge={"eq": [("weight",), 2]})  # node 1
        )
    )  # 1-3
    assert len(result) == 1
    assert result[0] == [1, 3]

    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},  # node 1
            PathCriteria(edge={"eq": [("weight",), 2]}, target={"eq": [("product",), "c"]}),  # 1-3  # 3
        )
    )
    assert len(result) == 1
    assert result[0] == [1, 3]


def test_search_relationships_nodes():
    g = build_graph()
    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},  # node 1
            PathCriteria(target={}, edge={"eq": [("weight",), 2]}),  # edge 1 - 3
            PathCriteria(target={"eq": [("product",), "d"]}),  # node 4
        )
    )
    assert result
    assert len(result) == 1
    assert result[0] == [1, 3, 4]


def test_search_relationships_nodes_multi_path():
    g = nx.DiGraph(build_graph())

    g.add_node(5, product="d")
    g.add_node(6, product="d")
    g.add_node(7, product="a")
    g.add_node(8, product="a")

    g.add_edge(7, 5, weight=2)
    g.add_edge(7, 6, weight=2)
    g.add_edge(8, 5, weight=2)

    assert len(list(search_relationships(g, {"eq": [("product",), "a"]}))) == 6

    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},  # node 1, 7, 8
            PathCriteria(
                target={"eq": [("product",), "d"]}, edge={"eq": [("weight",), 2]}
            ),  # edge 1-3, 7-5, 7-6, 8-5  node 4, 5, 6 -> no 1, 3, 4
        )
    )

    assert result
    assert len(result) == 3
    assert result == [[7, 5], [7, 6], [8, 5]]

    result = list(
        search_relationships(
            g,
            {"eq": [("product",), "a"]},  # node 1, 7, 8
            PathCriteria(target={}, edge={"eq": [("weight",), 2]}),  # edge 1-3, 7-5, 7-6, 8-5
            PathCriteria(target={"eq": [("product",), "d"]}),  # node 4, 5, 6 -> no 1, 3, 4
        )
    )

    assert result
    assert len(result) == 1
    assert result == [[1, 3, 4]]
