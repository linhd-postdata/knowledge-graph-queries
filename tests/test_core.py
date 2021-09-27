from knowledge_graph_queries.core import get_authors


def test_get_authors(snapshot):
    output = get_authors()
    snapshot.assert_match(output)
