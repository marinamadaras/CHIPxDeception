def test_hello(client):
    response = client.get('/')

    assert b'Hello' in response.data


def test_log(client):
    logged_line = b'blabla'
    response = client.get(f"/log/{logged_line}")

    assert logged_line in response.data


def test_get_log(client):
    logged_line_1 = 'blabla'
    logged_line_2 = 'test test'
    client.get(f"/log/{logged_line_1}")
    client.get(f"/log/{logged_line_2}")
    response = client.get("/log")
    lines = response.get_json()

    assert logged_line_1 in lines[0]
    assert logged_line_2 in lines[1]
