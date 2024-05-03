from flask import Flask, request
import requests
import json
from reason_advice import reason_advice
from reason_question import reason_question

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return 'Hello, I am the reasoning module!'


@app.route('/query-knowledge', methods=['POST'])
def query_knowledge():
    pass


@app.route('/store-knowledge', methods=['POST'])
def store_knowledge():
    print(f"Triples received: {request.json}", flush=True)

    # STORE KNOWLEDGE - Still unclear how to do this via API
    # res = requests.post(f'http://knowledge:7200/rest/????????????')

    # IF DONE, START REASONING (should query knowledge base somehow)
    reason_and_notify_response_generator()

    return 'OK'


# Note that we first check if we can give advice, and if that is "None",
# then we try to formulate a question instead. 
def reason_and_notify_response_generator():
    response = reason_advice()
    reason_type = "A"
    if (not response):
        reason_type = "Q"
        response = reason_question()

    # SEND REASONING RESULT
    payload = {"type": reason_type, "data": response}
    requests.post("http://response-generator:5000/submit-reasoner-response", json=payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
