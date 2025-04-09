from unittest.mock import Mock, patch, ANY
from app.tests.conftest import AnyStringWith


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_store_knowledge_empty(client, triples):
    res = client.post(f"/store", json=triples.empty)
    assert res.status_code == 200


def test_store_knowledge_success(client, util, triples):
    res = client.post(f"/store", json=triples.one)
    util.store_knowledge.assert_called_once()
    assert res.status_code == 200


def test_store_knowledge_inference_failed(client, util, triples):
    util.store_knowledge.side_effect = RuntimeError('Test')
    res = client.post(f"/store", json=triples.one)
    util.store_knowledge.assert_called_once()
    assert not res.status_code < 400  # Equivalent of requests.Response.ok
