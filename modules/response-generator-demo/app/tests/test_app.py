from unittest.mock import patch


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_submit_reasoner_response(client, reasoner_response):
    with patch('app.util') as util:
        client.post(f"/process", json=reasoner_response.question)
        util.send_message.assert_called_once()


