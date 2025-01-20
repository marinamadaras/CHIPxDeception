import pytest
from app import create_app
from unittest.mock import Mock, MagicMock, patch


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


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
def message_data():
    return {'message': "Some message!"}


@pytest.fixture()
def sentence_data():
    return {'sentence': "Some message!", 'patient_name': 'John', 'timestamp': ''}