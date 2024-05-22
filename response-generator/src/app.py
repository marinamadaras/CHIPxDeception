from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.debug = True

# Example of data
sentence_data = {"triples":{"subject": "Julia",
                            "object": "medicine",
                            "predicate": "hasPreference"}}

reasoner_response = {"type": "A",
                    "data": "medicine"}


def generate_response(sentence_data, reasoner_response):
    sub = sentence_data["triples"]["subject"]
    obj = sentence_data["triples"]["object"]
    pred = sentence_data["triples"]["predicate"]

    response_type = reasoner_response["type"]
    response_data = reasoner_response["data"]

    if response_type == "Q":
        return f"{sub}, {response_data}?"
    elif response_type == "A":
        return f"{sub}" has a preference for {response_data}.
    else:
        return "Invalid response."


def check_responses():
    global reasoner_response, sentence_data
    if reasoner_response and sentence_data:
        print("Got both sentence and reasoning, sending reply...", flush=True)
        reply = generate_response(reasoner_response, sentence_data)
        reasoner_response = None
        sentence_data = None
        payload = {"reply": reply}
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


@app.route('/ping/<name>')
def ping(name):
    r = requests.get(f'http://{name}:5000/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
