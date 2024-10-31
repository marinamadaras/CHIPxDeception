from unittest.mock import ANY, patch, MagicMock
from flask import g
from app.reason_question import get_missing_facts, get_required_facts, query_for_presence, reason_question, rule_based_question
from SPARQLWrapper import JSON
from app.tests.conftest import AnyStringWith


def test_reason_question(application, get_db_connection):
    with application.app_context():
        ret = reason_question()
        assert 'data' in ret


def test_rule_based_question_empty(application, test_name):
    with application.app_context(), \
            patch('app.reason_question.get_required_facts') as req, \
            patch('app.reason_question.get_missing_facts') as mis,  \
            patch('app.reason_question.sort_missing_facts') as srt:

        srt.return_value = []

        mf = rule_based_question(test_name)

        req.assert_called_once()
        mis.assert_called_once()
        srt.assert_called_once()

        assert mf is None


def test_rule_based_question_non_empty(application, test_name):
    with application.app_context(), \
            patch('app.reason_question.get_required_facts') as req, \
            patch('app.reason_question.get_missing_facts') as mis,  \
            patch('app.reason_question.sort_missing_facts') as srt:

        mock = MagicMock()
        srt.return_value = [mock]

        mf = rule_based_question(test_name)

        req.assert_called_once()
        mis.assert_called_once()
        srt.assert_called_once()

        assert mf is mock


def test_query_for_presence(application, get_db_connection):
    with application.app_context():
        _, conn = get_db_connection
        fact = 'test'
        query_ret = MagicMock()
        conn.query.return_value = query_ret

        query_for_presence(fact)

        conn.setQuery.assert_called_once_with(AnyStringWith(fact))
        conn.setReturnFormat.assert_called_once_with(JSON)
        conn.addParameter.assert_called_once_with(ANY, AnyStringWith('json'))
        conn.query.assert_called_once()
        query_ret.convert.assert_called()


# All the queries should operate on the given user's KG
def test_get_required_facts(application, test_name):
    with application.app_context():
        ret = get_required_facts(test_name)
        for query in ret:
            assert f'userKG:{test_name}' in query


def test_get_missing_facts_empty(application):
    with application.app_context():
        ret = get_missing_facts([])
        assert ret == []


def test_get_missing_facts_missing(application):
    with application.app_context(), patch('app.reason_question.query_for_presence') as qfp:
        fact = 'test'
        qfp_ret = False
        qfp.return_value = qfp_ret
        ret = get_missing_facts([fact])
        qfp.assert_called_with(fact)
        assert fact in ret


def test_get_missing_facts_present(application):
    with application.app_context(), patch('app.reason_question.query_for_presence') as qfp:
        fact = 'test'
        qfp_ret = True
        qfp.return_value = qfp_ret
        ret = get_missing_facts([fact])
        qfp.assert_called_with(fact)
        assert fact not in ret
        assert len(ret) == 0
