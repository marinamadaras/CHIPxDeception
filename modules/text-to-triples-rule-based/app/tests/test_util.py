from unittest.mock import patch, ANY
from app.util import send_triples, extract_triples, postprocess_triple
from app.tests.conftest import AnyStringWith, create_triple


def test_send_triples(application, sample_sentence_data, reasoner_address):
    with application.app_context(), \
            patch('app.util.extract_triples') as et, \
            patch('app.util.requests') as r:

        send_triples(sample_sentence_data)

        et.assert_called_once_with(sample_sentence_data)
        r.post.assert_called_once_with(AnyStringWith(reasoner_address), json=ANY)


def test_extract_triples_no_tokens(application, sample_sentence_data, sample_sentence):
    with application.app_context(), patch('app.util.postprocess_triple') as pt, patch('app.util.nltk') as nltk:
        nltk.pos_tag.return_value = []

        ret = extract_triples(sample_sentence_data)
        nltk.word_tokenize.assert_called_once_with(sample_sentence)
        pt.assert_not_called()
        assert 'triples' in ret


def test_extract_triples_no_predicate(application, sample_sentence_data, sample_sentence, sample_tokens):
    with application.app_context(), patch('app.util.postprocess_triple') as pt, patch('app.util.nltk') as nltk:
        nltk.pos_tag.return_value = sample_tokens[1:]

        ret = extract_triples(sample_sentence_data)
        nltk.word_tokenize.assert_called_once_with(sample_sentence)
        pt.assert_not_called()
        assert 'triples' in ret


def test_extract_triples(application, sample_sentence_data, sample_name, sample_sentence, sample_tokens):
    with application.app_context(), patch('app.util.postprocess_triple') as pt, patch('app.util.nltk') as nltk:
        nltk.pos_tag.return_value = sample_tokens

        ret = extract_triples(sample_sentence_data)
        nltk.word_tokenize.assert_called_once_with(sample_sentence)
        pt.assert_called_once_with(ANY, sample_name)
        assert 'triples' in ret


# Will not test the specifics yet, as it is all hard-coded.
def test_postprocess_triple(application, sample_name):
    with application.app_context():
        triple = create_triple('foo', 'bar', 'baz')
        ret = postprocess_triple(triple, sample_name)
        for key in triple:
            assert key in ret
