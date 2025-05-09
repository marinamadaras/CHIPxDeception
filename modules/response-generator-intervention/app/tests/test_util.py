from unittest.mock import Mock, patch
import app.util as util

def test_check_responses_both_set(application, reasoner_response):
    with application.app_context(), patch('app.util.generate_response'):
        # util.generate_response = Mock()
        # util.sentence_data = sentence_data.greet
        # util.reasoner_response = reasoner_response.question
        # util.check_responses()
        util.send_message(reasoner_response)

        util.generate_response.assert_called_once()

        # # Secondly it should reset the values of both sentence_data and reasoner_response
        # assert util.sentence_data is None
        # assert util.reasoner_response is None


# NOTE: Need an API key to test response generation with, not viable for now, and also not very useful.

# # A greeting is sent back upon greeting, no question or advice formulated
# def test_generate_response_greeting(application, reasoner_response):
#     with application.app_context(), patch('app.util.formulate_advice'), patch('app.util.formulate_question'):
#         res = util.generate_response(reasoner_response.greet)

#         util.formulate_question.assert_not_called()
#         util.formulate_advice.assert_not_called()
#         assert "hi" in res.lower()


# # A question is formulated if the reasoner comes up with a question.
# def test_generate_response_question(application, reasoner_response):
#     with application.app_context(), patch('app.util.formulate_advice'), patch('app.util.formulate_question'):
#         res = util.generate_response(reasoner_response.question)

#         util.formulate_question.assert_called_once()
#         util.formulate_advice.assert_not_called()
#         assert "?" in res.lower()


# # Advice is formulated if the reasoner comes up with advice.
# def test_generate_response_advice(application, reasoner_response):
#     with application.app_context(), patch('app.util.formulate_advice'), patch('app.util.formulate_question'):
#         res = util.generate_response(reasoner_response.advice)

#         util.formulate_question.assert_not_called()
#         util.formulate_advice.assert_called_once()
#         assert "activity" in res.lower()


# # Missing patient_name should result in "Unknown patient" being used as name.
# def test_generate_response_no_patient(application, sentence_data, reasoner_response):
#     with application.app_context(), patch('app.util.formulate_advice'), patch('app.util.formulate_question'):
#         del sentence_data.greet["patient_name"]
#         res = util.generate_response(reasoner_response.greet)
#         assert "Unknown Patient".lower() in res.lower()


