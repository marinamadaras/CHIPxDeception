import pytest
from app import create_app
from unittest.mock import Mock, MagicMock, patch
from types import SimpleNamespace


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@pytest.fixture()
def application(monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_ADDRESS", "dummy")
    app = create_app(test=True)
    # For detecting errors and disabling logging in general
    setattr(app, "logger", Mock(app.logger))
    yield app


@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def util():
    with patch('app.util') as util:
        yield util


@pytest.fixture()
def reason_question():
    with patch('app.util.reason_question') as reason_question:
        yield reason_question


@pytest.fixture()
def reason_advice():
    with patch('app.util.reason_advice') as reason_advice:
        yield reason_advice


@pytest.fixture()
def get_db_connection():
    with patch('app.db.get_db_connection') as get_db_connection:
        conn = MagicMock()
        get_db_connection.return_value = conn
        yield get_db_connection, conn


@pytest.fixture()
def triples():
    tr = SimpleNamespace()
    tr.empty = {'triples': []}
    tr.one = {'triples': [{"subject": "foo", "predicate": "bar", "object": "baz"}]}
    tr.many = {'triples': 3*[{"subject": "foo", "predicate": "bar", "object": "baz"}]}
    return tr


@pytest.fixture()
def test_name():
    return 'FooBarBaz'
