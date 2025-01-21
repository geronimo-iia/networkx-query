import networkx as nx

from networkx_query import prepare_query, search_edges, search_nodes

g = nx.DiGraph()
g.add_node(1, product="chocolate")
g.add_node(2, product="milk")
g.add_node(3, product="coat")
g.add_edge(1, 2, action="shake")
g.add_edge(3, 2, action="produce")


def test_prepare_query():
    predicate = prepare_query({"eq": [("product",), "chocolate"]})
    assert predicate({"product": "chocolate"})
    assert not predicate({"product": "milk"})


def test_search_nodes_implementation():
    predicate = prepare_query({"eq": [("product",), "chocolate"]})
    assert [(node[0], predicate(node[1])) for node in g.nodes(data=True)] == [(1, True), (2, False), (3, False)]


def test_search_edges_implementation():
    predicate = prepare_query({"eq": [("action",), "shake"]})
    assert [((edge[0], edge[1]), predicate(edge[2])) for edge in g.edges(data=True)] == [
        ((1, 2), True),
        ((3, 2), False),
    ]


def test_search_nodes():
    assert list(search_nodes(g, {"eq": [("product",), "chocolate"]})) == [1]
    assert list(search_nodes(g, {"eq": [("product",), "milk"]})) == [2]

    result = list(search_nodes(g, {"in": [("product",), ["milk", "coat"]]}))
    assert len(result) == 2
    assert 2 in result
    assert 3 in result

    assert list(search_nodes(g, {"eq": [("product",), "none"]})) == []


def test_search_edges():
    assert list(search_edges(g, {"eq": [("action",), "produce"]})) == [(3, 2)]
    assert list(search_edges(g, {"eq": [("action",), "shake"]})) == [(1, 2)]
    assert list(search_edges(g, {"eq": [("action",), "none"]})) == []
