from unittest.mock import Mock


# Confirm that check_responses doesn't do anything by itself
def test_check_responses_none(application, util):
    with application.app_context():
        util.generate_response = Mock()
        util.check_responses()
        util.generate_response.assert_not_called()


# Confirm that check_responses doesn't do anything with just sentence data
def test_check_responses_sentence_data(application, util, sentence_data):
    with application.app_context():
        util.generate_response = Mock()
        util.sentence_data = sentence_data.greet
        util.check_responses()
        util.generate_response.assert_not_called()


# Confirm that check_responses doesn't do anything with just a reasoner response
def test_check_responses_reasoner_response(application, util, reasoner_response):
    with application.app_context():
        util.generate_response = Mock()
        util.reasoner_response = reasoner_response.question
        util.check_responses()
        util.generate_response.assert_not_called()


# Confirm that something happens when both are set
def test_check_responses_both_set(application, util, sentence_data, reasoner_response):
    with application.app_context():
        util.generate_response = Mock()
        util.sentence_data = sentence_data.greet
        util.reasoner_response = reasoner_response.question
        util.check_responses()

        # First, it should generate a response
        util.generate_response.assert_called_once()

        # Secondly it should reset the values of both sentence_data and reasoner_response
        assert util.sentence_data is None
        assert util.reasoner_response is None


# A greeting is sent back upon greeting, no question or advice formulated
def test_generate_response_greeting(application, util, sentence_data, reasoner_response):
    with application.app_context():
        util.formulate_advice = Mock()
        util.formulate_question = Mock()
        res = util.generate_response(sentence_data.greet, reasoner_response.greet)

        util.formulate_question.assert_not_called()
        util.formulate_advice.assert_not_called()
        assert "hi" in res.lower()


# A question is formulated if the reasoner comes up with a question.
def test_generate_response_question(application, util, sentence_data, reasoner_response):
    with application.app_context():
        util.formulate_advice = Mock()
        util.formulate_question = Mock()
        res = util.generate_response(sentence_data.other, reasoner_response.question)

        util.formulate_question.assert_called_once()
        util.formulate_advice.assert_not_called()
        assert "?" in res.lower()


# Advice is formulated if the reasoner comes up with advice.
def test_generate_response_advice(application, util, sentence_data, reasoner_response):
    with application.app_context():
        util.formulate_advice = Mock()
        util.formulate_question = Mock()
        res = util.generate_response(sentence_data.other, reasoner_response.advice)

        util.formulate_question.assert_not_called()
        util.formulate_advice.assert_called_once()
        assert "activity" in res.lower()


# Missing patient_name should result in "Unknown patient" being used as name.
def test_generate_response_no_patient(application, util, sentence_data, reasoner_response):
    with application.app_context():
        util.formulate_advice = Mock()
        util.formulate_question = Mock()
        del sentence_data.greet["patient_name"]
        res = util.generate_response(sentence_data.greet, reasoner_response.greet)
        assert "Unknown Patient".lower() in res.lower()


