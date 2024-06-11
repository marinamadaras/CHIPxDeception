from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.debug = True

# Example of data
sentence_data = None

reasoner_response = None

GREETINGS = (
    "Hi",
    "Hello",
    "Yo"
)

def formulate_question(query: str) -> str:
    """
    Formulates a natural language question based on which facts are missing from the DB.
    """
    if 'prioritizedOver' in query:
        return "that depends on what you find important. What do you prioritize?"
    elif 'hasPhysicalActivityHabit' in query:
        return "what physical activities do you regularly do"
    raise ValueError(f"Cannot formulate question for query {query}")

def formulate_advice(activity: str) -> str:
    prefix = "http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#"
    activity = activity.replace(prefix, "")

    activity = activity.replace("_", " ")
    return activity

def generate_response(sentence_data, reasoner_response):
    try:
        name = sentence_data['patient_name']
    except KeyError:
        name = "Unknown patient"
    print(sentence_data, flush=True)
    response_type = reasoner_response["type"]
    response_data = reasoner_response["data"]

    if sentence_data['sentence'] in GREETINGS:
        return f"Hi, {name}"

    if response_type == "Q":
        question = formulate_question(response_data['data'])
        return f"{name}, {question}?"
    elif response_type == "A":
        activity = formulate_advice(response_data['data'][1])
        return f"How about the activity '{activity}', {name}?"
    else:
        return "Invalid response."


def check_responses():
    global reasoner_response, sentence_data
    if reasoner_response and sentence_data:
        print("Got both sentence and reasoning, sending reply...", flush=True)
        reply = generate_response(sentence_data, reasoner_response)
        reasoner_response = None
        sentence_data = None
        payload = {"reply": reply}
        print("response", payload, flush=True)
        requests.post("http://front-end:8000/response", json=payload)


@app.route('/subject-sentence', methods=['POST'])
def submit_sentence():
    global sentence_data
    data = request.json
    print(f"Received sentence: {data}", flush=True)
    sentence_data = data

    check_responses()

    return 'OK'


@app.route('/submit-reasoner-response', methods=['POST'])
def submit_reasoner_response():
    global reasoner_response
    data = request.json
    print(f"Received data from reasoner: {data}", flush=True)
    reasoner_response = data

    check_responses()

    return 'OK'

@app.route('/')
def hello():
    return 'Hello, I am the response generator module!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
