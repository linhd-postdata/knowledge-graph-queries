import json

import pytest

from knowledge_graph_queries import app


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as test_client:
        yield test_client


def test_get_authors(snapshot, client):
    response = client.get('/authors')
    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.data))
