from unittest.mock import patch, ANY
from app.util.db import get_db_connection
from app.tests.conftest import AnyStringWith


def test_get_db_connection(application):
    with patch('app.util.db.SPARQLWrapper.__new__') as SPARQLWrapper, application.app_context():
        get_db_connection()
        SPARQLWrapper.assert_called_once_with(
            ANY,
            AnyStringWith(application.config['knowledge_url'])
        )