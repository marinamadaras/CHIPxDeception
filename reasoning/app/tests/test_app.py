from unittest.mock import Mock, patch, ANY
from app.tests.conftest import AnyStringWith


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_store_knowledge_empty(client, util, triples):
    res = client.post(f"/store-knowledge", json=triples.empty)

    util.reason.assert_called_once()
    assert b"empty" in res.data.lower()
    assert res.status_code == 200


def test_store_knowledge_success(client, util, triples):
    knowledge_res = Mock()
    knowledge_res.status_code = 204
    util.upload_rdf_data.return_value = knowledge_res

    res = client.post(f"/store-knowledge", json=triples.one)

    util.reason.assert_called_once()
    util.json_triple_to_rdf.assert_called_once()
    assert res.status_code == 200


def test_store_knowledge_inference_failed(client, util, triples):
    res = client.post(f"/store-knowledge", json=triples.one)

    util.reason.assert_called_once()
    util.json_triple_to_rdf.assert_called_once()
    assert res.status_code == 500


def test_reason_and_notify_response_generator(client, util, monkeypatch):
    with patch('app.routes.requests') as r:
        dummy_url = 'dummy'
        monkeypatch.setenv('RESPONSE_GENERATOR_ADDRESS', dummy_url)
        res = client.get(f"/reason")
        util.reason.assert_called_once()
        r.post.assert_called_once_with(AnyStringWith(dummy_url), json=ANY)
        assert res.status_code == 200
