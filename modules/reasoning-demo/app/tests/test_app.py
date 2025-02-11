from unittest.mock import Mock, patch, ANY
from app.tests.conftest import AnyStringWith


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_store_knowledge_empty(client, util, sample_t2t_data):
    res = client.post(f"/store-knowledge", json=sample_t2t_data.empty)
    util.reason_and_notify_response_generator.assert_called_once()

    assert b"empty" in res.data.lower()
    assert res.status_code == 200


def test_store_knowledge_success(client, util, sample_t2t_data):
    knowledge_res = Mock()
    knowledge_res.status_code = 204
    util.upload_rdf_data.return_value = knowledge_res

    res = client.post(f"/store-knowledge", json=sample_t2t_data.one)

    util.reason_and_notify_response_generator.assert_called_once()
    util.json_triple_to_rdf.assert_called_once()
    assert res.status_code == 200


def test_store_knowledge_inference_failed(client, util, sample_t2t_data):
    ret = Mock()
    ret.status_code = 500
    ret.text = "blabla"
    util.upload_rdf_data.return_value = ret

    res = client.post(f"/store-knowledge", json=sample_t2t_data.one)

    util.reason_and_notify_response_generator.assert_called_once()
    util.json_triple_to_rdf.assert_called_once()
    assert not res.status_code < 400  # Equivalent of requests.Response.ok
