from unittest.mock import patch


def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_new_sentence(client, sample_name, sample_sentence):
    with patch('app.util.send_triples') as st:
        res = client.post('/new-sentence', json={
            'sentence': sample_sentence,
            'patient_name': sample_name
        })
        st.assert_called_once()
        assert res.status_code == 200
