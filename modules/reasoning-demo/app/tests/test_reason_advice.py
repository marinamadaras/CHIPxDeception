from unittest.mock import ANY, patch
from flask import g
from app.reason_advice import reason_advice, recommended_activities_sorted, rule_based_advice
from SPARQLWrapper import JSON
from app.tests.conftest import AnyStringWith


def test_reason_advice(application, get_db_connection, sample_name):
    with application.app_context():
        ret = reason_advice(sample_name)
        assert 'data' in ret


def test_recommended_activities_sorted(application, get_db_connection, sample_name):
    with application.app_context():
        _, conn = get_db_connection

        recommended_activities_sorted(sample_name)

        conn.setQuery.assert_called_once()
        conn.setReturnFormat.assert_called_once_with(JSON)
        conn.addParameter.assert_called_once_with(ANY, AnyStringWith('json'))


def test_rule_based_advice(application, sample_name):
    with application.app_context(), patch('app.reason_advice.recommended_activities_sorted') as rec:
        rule_based_advice(sample_name)
        rec.assert_called_once_with(sample_name)
