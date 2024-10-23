import pytest
from app import create_app
from unittest.mock import Mock
from types import SimpleNamespace


@pytest.fixture()
def util():
    import sys
    del sys.modules['app.util']
    import app.util
    return app.util


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
def reasoner_response():
    rr = SimpleNamespace()
    rr.greet = {"data": None, "type": "Q"}
    rr.question = {"data": {"data": "prioritizedOver"}, "type": "Q"}
    rr.advice = {"data": {"data": [None, "some activity"]}, "type": "A"}
    return rr
