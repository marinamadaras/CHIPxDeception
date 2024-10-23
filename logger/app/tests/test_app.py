from logging import StreamHandler


def test_hello(client):
    response = client.get('/')

    assert b'Hello' in response.data


def test_log(client):
    logged_line = b'blabla'
    response = client.get(f"/log/{logged_line}")

    assert logged_line in response.data


def test_log_post(client):
    logged_line = b'blabla'
    response = client.post(f"/log", data={
        "msg": logged_line,
        "service_name": "service",
        "levelno": 0
    })

    assert logged_line in response.data


def test_get_log_file(client):
    logged_line_1 = 'blabla'
    logged_line_2 = 'test test'
    client.get(f"/log/{logged_line_1}")
    client.get(f"/log/{logged_line_2}")
    response = client.get("/log")
    lines = response.get_json()

    assert logged_line_1 in lines[0]
    assert logged_line_2 in lines[1]

    # Still works after inserting adding a different handler
    logged_line_3 = 'hurray'
    handler = StreamHandler()
    client.application.logger.handlers.insert(0, handler)
    client.get(f"/log/{logged_line_3}")
    another_response = client.get("/log")
    more_lines = another_response.get_json()
    assert logged_line_3 in more_lines[2]


def test_get_log_file_not_exist(client):
    client.application.logger.handlers = []
    response = client.get("/log")
    assert response.status_code == 503
