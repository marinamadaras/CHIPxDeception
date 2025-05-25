from flask import current_app
import app
import requests


def reason(sentence_data):
    sentence = sentence_data['sentence']    
    
    response = app.reasoner.process_input(sentence)

    current_app.logger.warn(f"1233456789 Turn count {app.reasoner.turn_count}")
    current_app.logger.info(f"reasoning result: {response}")
    return response


# sentence data is of type json
def reason_and_notify_response_generator(sentence_data):
    payload = reason(sentence_data)
    payload['sentence_data'] = sentence_data

    response_generator_address = current_app.config.get("RESPONSE_GENERATOR_ADDRESS", None)
    if response_generator_address:
        requests.post(f"http://{response_generator_address}/process", json=payload)
