import pytest
from app import create_app
from unittest.mock import Mock, MagicMock, patch
from types import SimpleNamespace


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@pytest.fixture()
def response_generator_address():
    return "dummy_response_generator"


@pytest.fixture()
def knowledge_address():
    return "dummy_knowledge"



@pytest.fixture()
def application(monkeypatch, response_generator_address, knowledge_address):
    monkeypatch.setenv("KNOWLEDGE_DEMO", knowledge_address)
    monkeypatch.setenv("RESPONSE_GENERATOR_MODULE", "TEST_MOD_1")
    monkeypatch.setenv("TEST_MOD_1", response_generator_address)
    app = create_app(test=True)
    # For detecting errors and disabling logging in general
    setattr(app, "logger", Mock(app.logger))
    app.config["DEBUG"] = True  # Actually give stack-traces on client failures.
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
def reason():
    with patch('app.util.reason') as reason_advice:
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
def sample_sentence():
    return "Some cool sentence."


@pytest.fixture()
def sample_name():
    return 'SomeRandomName'


@pytest.fixture()
def sample_timestamp():
    return '...'


@pytest.fixture()
def sample_sentence_data(sample_sentence, sample_name, sample_timestamp):
    return {
        'patient_name': sample_name,
        'sentence': sample_sentence,
        'timestamp': sample_timestamp
    }


@pytest.fixture()
def sample_t2t_data(sample_sentence_data, triples):
    t2t = SimpleNamespace()
    sentence_data = {'sentence_data': sample_sentence_data}
    t2t.empty = triples.empty | sentence_data
    t2t.one = triples.one | sentence_data
    t2t.many = triples.many | sentence_data
    return t2t
