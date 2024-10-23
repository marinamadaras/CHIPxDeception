from unittest.mock import patch


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_subject_sentence(client, sentence_data):
    with patch('app.util') as util:
        client.post(f"/subject-sentence", json=sentence_data.greet)

        assert type(util.sentence_data) is dict
        assert type(util.reasoner_response) is not dict
        util.check_responses.assert_called_once()


def test_submit_reasoner_response(client, reasoner_response):
    with patch('app.util') as util:
        client.post(f"/submit-reasoner-response", json=reasoner_response.question)

        assert type(util.sentence_data) is not dict
        assert type(util.reasoner_response) is dict
        util.check_responses.assert_called_once()


