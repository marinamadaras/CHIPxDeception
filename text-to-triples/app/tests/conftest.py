import pytest
from app import create_app
from unittest.mock import Mock
# from types import SimpleNamespace


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


def create_triple(subj, pred, obj):
    return {"subject": subj, "object": obj, "predicate": pred}


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
def sample_name():
    return 'John'


@pytest.fixture()
def sample_sentence():
    return 'Some cool sentence.'


@pytest.fixture()
def sample_tokens():
    return [('foo', 'VB'), ('bar', 'NN'), ('baz', 'NN')]
