import pytest
from app import create_app
from unittest.mock import Mock, MagicMock, patch
from types import SimpleNamespace


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


