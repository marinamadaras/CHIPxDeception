def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data


def test_log(client):
    logged_line = b'blabla'
    response = client.get(f"/log/{logged_line}")
    assert logged_line in response.data
