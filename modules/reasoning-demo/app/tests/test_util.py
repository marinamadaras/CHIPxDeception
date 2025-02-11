from unittest.mock import Mock, patch, ANY
from app.util import json_triple_to_rdf, upload_rdf_data, reason, reason_and_notify_response_generator
from app.tests.conftest import AnyStringWith


def test_json_triple_to_rdf(triples, application):
    with patch('app.util.Graph.__new__') as Graph, application.app_context():
        graph = Mock()
        Graph.return_value = graph
        single_triple = triples.one['triples'][0]

        # Call the method
        json_triple_to_rdf(single_triple)

        # Assert that a new graph was made, and that the triple was added appropriately
        Graph.assert_called_once()
        graph.add.assert_called_with((
                AnyStringWith(single_triple['subject']),
                AnyStringWith(single_triple['predicate']),
                AnyStringWith(single_triple['object'])
        ))


def test_json_triple_to_rdf_serialization_result(triples, application):
    with application.app_context():
        single_triple = triples.one['triples'][0]

        # Call the method
        ret = json_triple_to_rdf(single_triple)

        # Check whether our serialized result contains the things we want
        assert '@prefix' in ret
        assert "userKG" in ret
        for v in single_triple.values():
            assert v in ret


def test_upload_rdf_data(application):
    with patch("app.util.requests.post") as post, application.app_context():
        res = Mock()
        res.ok = True
        post.return_value = res
        rdf_data = Mock()

        # Call the method
        upload_rdf_data(rdf_data)

        # Posted with the correct data
        post.assert_called_with(ANY, data=rdf_data, headers=ANY)

        # And confirm we didn't log an error, because the post was succesful
        application.logger.error.assert_not_called()


def test_upload_rdf_data_error(application):
    with patch("app.util.requests.post") as post, application.app_context():
        res = Mock()
        res.ok = False
        post.return_value = res

        # Call the method
        upload_rdf_data(Mock())

        # Confirm that we logged an error because the post failed
        application.logger.error.assert_called()


def test_upload_rdf_data_no_knowledge(application):
    with patch("app.util.requests.post") as post, application.app_context():
        application.config['knowledge_url'] = None

        # Call the method
        res = upload_rdf_data(Mock())

        # Confirm that we return a 503 due to missing knowledge DB
        assert res.status_code == 503


def test_reason_advice_success(application, reason_advice, reason_question):
    with application.app_context():
        reason_advice.return_value = {'data': True}

        # Call the method
        ret = reason()

        # Confirm that we will not reason for formulating a question if advice succeeded
        reason_advice.assert_called_once()
        reason_question.assert_not_called()
        assert ret['type'] == 'A'
        assert 'data' in ret


def test_reason_advice_failure(application, reason_advice, reason_question):
    with application.app_context():
        reason_advice.return_value = {'data': False}

        # Call the method
        ret = reason()

        # Confirm that we reason for a question since advice failed
        reason_advice.assert_called_once()
        reason_question.assert_called_once()
        assert ret['type'] == 'Q'
        assert 'data' in ret


def test_reason_and_notify_response_generator(application, sample_sentence_data, response_generator_address, reason):
    with patch('app.util.requests') as r, application.app_context():
        reason.return_value = {}
        reason_and_notify_response_generator(sample_sentence_data)
        reason.assert_called_once()
        r.post.assert_called_once_with(AnyStringWith(response_generator_address), json=ANY)