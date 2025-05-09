from flask import current_app
from enum import auto
from strenum import StrEnum
import requests
import app


GREETINGS = {
    "hi",
    "hello", 
    "hey", 
    "good morning", 
    "good night"}

CLOSING = (
    "bye",
    "thanks",
    "thank you",
    "goodbye"
)

class ResponseType(StrEnum):
    Q = auto()
    A = auto()
    G = auto() # greeting, goes beyond just saying hi back
    C = auto() # closing


# This method takes the reasoner_response, and splits it into:
# [] sentence_data: a dictionary of the name, timestamp and the sentence typed by the user
# [] response_type: which initially comes from the reasoner as either:
#                    -> Q from a question
#                    -> A from advice
#                  but, it is extended with G from greeting and C from closing statement
# [] response_data: a dictionary with all the data resulting from the reasoning process
# This method then delegates the generation of the response to the framed response generator
# which pieces together all this data into natural language, through a specific
# framing strategy (e.g. neutral)
def generate_response(reasoner_response):
    sentence_data = reasoner_response['sentence_data']

    response_type = ResponseType(reasoner_response["type"])
    response_data = reasoner_response["data"]

    if sentence_data['sentence'].lower() in GREETINGS: # todo: make this more robust
        response_type = ResponseType.G
    elif sentence_data['sentence'].lower() in CLOSING:
        response_type = ResponseType.C    
    # response_type = ResponseType.A

    response_framer = app.response_framer.get()

    return response_framer.generate_response(
            response_data,
              sentence_data,
                response_type)


# This takes the input from the reasoner, creates a
# message for the user through LLM and sends it
# to the frontend module :)
def send_message(reasoner_response):
    current_app.logger.debug(f"-------------REASONER RESPONSE: {reasoner_response}")
    message = generate_response(reasoner_response)
    payload = {"message": message}
    current_app.logger.debug(f"sending response message: {payload}")
    front_end_address = current_app.config.get("FRONTEND_ADDRESS", None)
    if front_end_address:
        requests.post(f"http://{front_end_address}/process", json=payload)

