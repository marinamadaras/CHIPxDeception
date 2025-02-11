from unittest.mock import patch, ANY
from app.util import send_triples
from app.tests.conftest import AnyStringWith, create_triple


def test_send_triples(application, sample_sentence_data, reasoner_address):
    with application.app_context(), \
            patch('app.util.process_input_output') as et, \
            patch('app.util.requests') as r:

        send_triples(sample_sentence_data)

        et.assert_called_once_with(sample_sentence_data)
        r.post.assert_called_once_with(AnyStringWith(reasoner_address), json=ANY)

