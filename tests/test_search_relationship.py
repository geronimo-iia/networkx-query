import networkx as nx

from networkx_query.query import search_direct_relationships


g = nx.DiGraph()
for i in range(30):
    g.add_node(i, data=i)

for i in range(10, 30):
    g.add_edge(i - 10, i, data=i)


def test_search_direct_relationships_default():
    assert search_direct_relationships(g) == g.edges


def test_search_direct_relationships_free_edge_and_tail():
    assert list(search_direct_relationships(graph=g, source={"lt": ["data", 3]})) == [(0, 10), (1, 11), (2, 12)]


def test_search_direct_relationships_free_tail():
    assert list(search_direct_relationships(graph=g, source={"lt": ["data", 5]}, edge={"gt": ["data", 15]})) == []

    assert list(search_direct_relationships(graph=g, source={"lt": ["data", 8]}, edge={"gt": ["data", 15]})) == [
        (6, 16),
        (7, 17),
    ]


def test_search_direct_relationships():
    assert list(
        search_direct_relationships(
            graph=g, source={"gt": ["data", 9]}, edge={"gt": ["data", 15]}, target={'lt': ["data", 22]}
        )
    ) == [(10, 20), (11, 21)]
