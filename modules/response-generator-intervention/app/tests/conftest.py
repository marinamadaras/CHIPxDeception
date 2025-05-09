import pytest
from app import create_app
from unittest.mock import Mock, patch
from types import SimpleNamespace


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@pytest.fixture()
def util():
    with patch('app.util') as util:
        yield util


@pytest.fixture()
def application():
    yield create_app(test=True)


@pytest.fixture()
def client(application):
    tc = application.test_client()
    # For detecting errors and disabling logging in general
    setattr(tc.application, "logger", Mock(tc.application.logger))
    return tc


@pytest.fixture()
def sentence_data():
    sd = SimpleNamespace()
    patient_name = "Tim"
    sd.greet = {"sentence": "Hi", "patient_name": patient_name}
    sd.other = {"sentence": "Something else", "patient_name": patient_name}
    return sd


@pytest.fixture()
def reasoner_response(sentence_data):
    rr = SimpleNamespace()
    rr.greet = {"data": None, "type": "Q", "sentence_data": sentence_data.greet}
    rr.question = {"data": {"data": "prioritizedOver"}, "type": "Q", "sentence_data": sentence_data.other}
    rr.advice = {"data": {"data": [None, "some activity"]}, "type": "A", "sentence_data": sentence_data.other}
    return rr
