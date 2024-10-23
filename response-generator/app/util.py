from flask import current_app
from enum import auto
from strenum import StrEnum
import requests
import os



reasoner_response = None
sentence_data = None

GREETINGS = (
    "Hi",
    "Hello",
    "Yo"
)


class ResponseType(StrEnum):
    Q = auto()
    A = auto()


def formulate_question(query: str) -> str:
    """
    Formulates a natural language question based on which facts are missing from the DB.
    """
    if 'prioritizedOver' in query:
        return "that depends on what you find important. What do you prioritize?"
    elif 'hasPhysicalActivityHabit' in query:
        return "what physical activities do you regularly do"
    raise ValueError(f"Cannot formulate question for query {query}")

# =============================================================================
# def formulate_advice(activity: str) -> str:
#     prefix = "http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#"
#     activity = activity.replace(prefix, "")
# 
#     activity = activity.replace("_", " ")
#     return activity
# =============================================================================


def formulate_advice(activity: str) -> str:
    prefix = "http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#"
    activity = activity.replace(prefix, "")

    # Split activity on underscore and take the last part if it starts with "activity"
    parts = activity.split("_")
    if parts[0] == "activity":
        activity = "_".join(parts[1:])

    activity = activity.replace("_", " ")
    return activity


def generate_response(sentence_data, reasoner_response):
    try:
        name = sentence_data['patient_name']
    except KeyError:
        name = "Unknown patient"
    current_app.logger.debug(f"sentence_data: {sentence_data}")
    response_type = reasoner_response["type"]
    response_data = ResponseType(reasoner_response["data"])

    if sentence_data['sentence'] in GREETINGS:
        return f"Hi, {name}"

    if response_type == ResponseType.Q:
        question = formulate_question(response_data['data'])
        return f"{name}, {question}?"
    elif response_type == ResponseType.A:
        activity = formulate_advice(response_data['data'][1])
        return f"How about the activity '{activity}', {name}?"


def check_responses():
    global reasoner_response, sentence_data
    if reasoner_response and sentence_data:
        current_app.logger.info("Got both sentence and reasoning, sending reply...")
        reply = generate_response(sentence_data, reasoner_response)
        reasoner_response = None
        sentence_data = None
        payload = {"reply": reply}
        current_app.logger.debug(f"response: {payload}")
        front_end_address = os.environ.get("FRONTEND_ADDRESS", None)
        if front_end_address:
            try:
                requests.post(f"http://{front_end_address}/response", json=payload)
            except Exception:
                current_app.logger.error("Could not reach front-end, is it running at the expected address?")