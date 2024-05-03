from flask import Flask, request
import requests
import json
from dataclasses import dataclass




app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return 'Hello, I am the text to triples module!'

@app.route('/new-sentence', methods=['POST'])
def new_sentence():
    data = request.json
    sentence = data["sentence"]
    patient_name = data['patient_name']
    print(f"Patient {patient_name} wrote {sentence}", flush=True)
    send_triples(patient_name, sentence)
    return 'OK'

def create_triple(subj, pred, obj):
    return {"subject":subj, "object":obj, "predicate":pred}

def infer_triples(patient_name, sentence):
    # Do something to infer triples here...
    # For now, a hard-coded response
    return [
        create_triple("Julia", "hasValue", "Family"),
        create_triple("Julia", "hasPreference", "NoMedication")
    ]

def send_triples(patient_name, sentence):
    triples = infer_triples(patient_name, sentence)
    payload = {"triples": triples}
    requests.post("http://reasoning:5000/store-knowledge", json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
